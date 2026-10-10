/* PT_ASKCLAUDE_V1 — "Ask Claude" for Progress Tracker (super admins only).
 *
 * The browser never sees the Anthropic key. This callable function:
 *   1. requires a signed-in caller who is listed in platform/config.superAdminUids,
 *   2. enforces a per-user daily request cap (aiUsage/{uid}_{date}),
 *   3. forwards the conversation + a data snapshot to Claude,
 *   4. returns Claude's text and any DRAFTS (priority / issue / update / person).
 * Nothing is written to Progress Tracker here. Drafts are applied in the browser,
 * through the app's own forms, under the signed-in user's own permissions.
 */
const { onCall, HttpsError } = require("firebase-functions/v2/https");
const { defineSecret, defineString } = require("firebase-functions/params");
const admin = require("firebase-admin");

admin.initializeApp();
const db = admin.firestore();

const ANTHROPIC_API_KEY = defineSecret("ANTHROPIC_API_KEY");
const CLAUDE_MODEL = defineString("CLAUDE_MODEL", { default: "claude-sonnet-5-5" });
const DAILY_LIMIT = 150;
const MAX_CONTEXT_CHARS = 400000;
const MAX_TURNS = 30;

const TOOLS = [
  {
    name: "draft_priority",
    description: "Draft a new priority for a person. The user reviews it before anything is saved. Priorities have no due-date field: put any timing in the note.",
    input_schema: {
      type: "object",
      properties: {
        ownerMid: { type: "string", description: "Member id (mid) of the person who owns the priority. Must be an id from the data." },
        title: { type: "string" },
        note: { type: "string", description: "Optional detail: why it matters, timing, success measure." },
        status: { type: "string", enum: ["Scoping", "Active", "Blocked", "Review"] },
        visibility: { type: "string", enum: ["private", "manager", "team", "everyone"], description: "private = owner (and admins); manager = owner and their manager; team = their team; everyone = whole company. Default private." },
        involves: { type: "array", items: { type: "string" }, description: "Member ids of others involved." }
      },
      required: ["ownerMid", "title"]
    }
  },
  {
    name: "draft_issue",
    description: "Draft a new issue. The user reviews it before anything is saved.",
    input_schema: {
      type: "object",
      properties: {
        title: { type: "string" },
        description: { type: "string" },
        targetType: { type: "string", enum: ["person", "function"], description: "Raise it to a specific person, or to a team/function (its leader is tagged)." },
        targetId: { type: "string", description: "mid of the person, or fid of the team, from the data." },
        raisedByMid: { type: "string", description: "mid of who the issue is from. Required." },
        kind: { type: "string", enum: ["action", "fyi"], description: "action = someone must act; fyi = information only. Default action." },
        visibility: { type: "string", enum: ["private", "teamleader", "participants", "dept", "leader", "team"], description: "private = raiser only; teamleader = raiser and the tagged person/leader; participants = those involved; dept = the department; leader = all leaders and the CEO; team = whole company. Default participants for a person, leader for a function. dept is only valid for a function." },
        others: { type: "array", items: { type: "string" }, description: "mids of other people to tag in." }
      },
      required: ["title", "targetType", "targetId", "raisedByMid"]
    }
  },
  {
    name: "draft_update",
    description: "Draft a progress update (a log message) on an existing priority or issue.",
    input_schema: {
      type: "object",
      properties: {
        onType: { type: "string", enum: ["priority", "issue"] },
        onId: { type: "string", description: "Id of the priority or issue from the data." },
        text: { type: "string" }
      },
      required: ["onType", "onId", "text"]
    }
  },
  {
    name: "draft_person",
    description: "Draft adding a new person to the company's org chart.",
    input_schema: {
      type: "object",
      properties: {
        first: { type: "string" },
        last: { type: "string" },
        email: { type: "string" },
        title: { type: "string", description: "Job title." },
        managerMid: { type: "string", description: "mid of who they report to. Omit for top level." },
        functionId: { type: "string", description: "fid of their team. Omit for no team." },
        isLeader: { type: "boolean", description: "True if they lead that team." }
      },
      required: ["first"]
    }
  }
];

function systemPrompt(companyName, today) {
  return [
    "You are Claude, built into Progress Tracker, a leadership tool from Performance Intelligence that companies use to track issues, priorities and their org chart.",
    "You are talking to a super admin (the coach who runs the platform). Today is " + today + ". The company in view is " + JSON.stringify(companyName) + ".",
    "",
    "DATA: The user's message is accompanied by a JSON snapshot of this company: people, teams, issues and priorities. Answer only from that snapshot. If something is not in it, say so plainly. Progress-log messages are not included, so you cannot see the discussion inside an issue or priority.",
    "Issue status values: open = Open, prog = In progress, done = Completed. ballMid is the person currently responsible for an action issue.",
    "",
    "REFERENCES: Whenever you mention a specific issue, priority or person, write it as a link token so the app can make it clickable:",
    "  [[issue:ID|Title]]   [[pri:ID|Title]]   [[person:MID|Name]]",
    "Use only ids that appear in the snapshot. Never invent an id.",
    "",
    "ADDING THINGS: When the user asks you to add, raise, create or log something, call the matching draft_ tool. The user sees a card and confirms it, so do not ask for confirmation in text first. Use ids from the snapshot. If an essential detail is genuinely ambiguous (for example two people share a first name), ask one short question instead of guessing. You may call several draft tools in one reply.",
    "",
    "STYLE: Be concise and direct. Short paragraphs; use '- ' bullets only for genuine lists. No headers. American English. No emoji."
  ].join("\n");
}

async function assertSuper(uid) {
  const snap = await db.doc("platform/config").get();
  const list = (snap.exists && snap.data().superAdminUids) || [];
  if (!Array.isArray(list) || list.indexOf(uid) < 0) {
    throw new HttpsError("permission-denied", "Ask Claude is available to super admins only.");
  }
}

async function countUsage(uid) {
  const day = new Date().toISOString().slice(0, 10);
  const ref = db.collection("aiUsage").doc(uid + "_" + day);
  await db.runTransaction(async (tx) => {
    const s = await tx.get(ref);
    const n = s.exists ? (s.data().count || 0) : 0;
    if (n >= DAILY_LIMIT) {
      throw new HttpsError("resource-exhausted", "Daily limit of " + DAILY_LIMIT + " questions reached. It resets at midnight UTC.");
    }
    tx.set(ref, { uid: uid, day: day, count: n + 1, updatedAt: admin.firestore.FieldValue.serverTimestamp() }, { merge: true });
  });
}

function cleanMessages(raw) {
  if (!Array.isArray(raw) || !raw.length) throw new HttpsError("invalid-argument", "No message.");
  const msgs = raw.slice(-MAX_TURNS).map((m) => ({
    role: m && m.role === "assistant" ? "assistant" : "user",
    content: String((m && m.content) || "").slice(0, 20000)
  })).filter((m) => m.content.trim());
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  // merge consecutive same-role turns (the API requires alternation)
  const out = [];
  msgs.forEach((m) => {
    if (out.length && out[out.length - 1].role === m.role) out[out.length - 1].content += "\n\n" + m.content;
    else out.push({ role: m.role, content: m.content });
  });
  if (!out.length || out[out.length - 1].role !== "user") throw new HttpsError("invalid-argument", "The last message must be from the user.");
  return out;
}

exports.askClaude = onCall(
  {
    region: "us-central1",
    secrets: [ANTHROPIC_API_KEY],
    timeoutSeconds: 120,
    memory: "256MiB",
    maxInstances: 5,
    cors: ["https://progress-tracker.live", "https://www.progress-tracker.live"]
  },
  async (request) => {
    if (!request.auth) throw new HttpsError("unauthenticated", "Please sign in.");
    const uid = request.auth.uid;
    await assertSuper(uid);

    const data = request.data || {};
    const messages = cleanMessages(data.messages);
    let context = String(data.context || "");
    if (context.length > MAX_CONTEXT_CHARS) context = context.slice(0, MAX_CONTEXT_CHARS) + "\n…(snapshot truncated)";
    const companyName = String(data.companyName || "this company").slice(0, 200);
    const today = String(data.today || new Date().toDateString()).slice(0, 60);

    // Put the snapshot in front of the newest user message.
    const last = messages[messages.length - 1];
    last.content = "<company_snapshot>\n" + context + "\n</company_snapshot>\n\n" + last.content;

    await countUsage(uid);

    let res;
    try {
      res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "x-api-key": ANTHROPIC_API_KEY.value(),
          "anthropic-version": "2023-06-01"
        },
        body: JSON.stringify({
          model: CLAUDE_MODEL.value(),
          max_tokens: 2000,
          system: systemPrompt(companyName, today),
          tools: TOOLS,
          messages: messages
        })
      });
    } catch (e) {
      console.error("anthropic fetch failed", e);
      throw new HttpsError("unavailable", "Couldn't reach Claude. Try again in a moment.");
    }
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      console.error("anthropic error", res.status, JSON.stringify(body).slice(0, 2000));
      const msg = (body && body.error && body.error.message) || ("HTTP " + res.status);
      throw new HttpsError(res.status === 429 ? "resource-exhausted" : "internal", "Claude returned an error: " + msg);
    }
    const blocks = Array.isArray(body.content) ? body.content : [];
    const text = blocks.filter((b) => b.type === "text").map((b) => b.text).join("\n\n").trim();
    const drafts = blocks
      .filter((b) => b.type === "tool_use" && /^draft_/.test(b.name || ""))
      .map((b) => ({ type: b.name.replace(/^draft_/, ""), input: b.input || {} }));
    return { text: text, drafts: drafts, model: body.model || null };
  }
);
