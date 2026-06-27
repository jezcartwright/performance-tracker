import sys
PATH="index.html"; SENTINEL="/* PL_ISS_SPOKE_FIX_V1 */"
EDITS=[
(".iss-spoke{margin-left:auto}",
 ".iss-spoke{display:inline-flex;align-items:center;gap:7px}.iss-spoke-lbl{font-size:11px;color:var(--t3)}"+SENTINEL),
("'<span class=\"iss-spoke\">'+spokenToggle(i)+'</span></div>'",
 "'<span class=\"iss-spoke\"><span class=\"iss-spoke-lbl\">Spoken</span>'+spokenToggle(i)+'</span></div>'"),
]
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change."); sys.exit(0)
for k,(o,n) in enumerate(EDITS):
    c=s.count(o)
    if c!=1:
        sys.stderr.write("ABORT edit %d: count=%d\n"%(k,c)); sys.exit(1)
    s=s.replace(o,n); print("  edit %d ok"%k)
open(PATH,"w",encoding="utf-8").write(s)
print("Applied PL_ISS_SPOKE_FIX_V1. New size: %d bytes."%len(s.encode("utf-8")))
