import sys
PATH="index.html"; SENTINEL="/* PL_ISS_SPOKE_LABEL_V1 */"
EDITS=[
("function spokenToggle(i){ var on=!!i.conversationHad;",
 "function spokenToggle(i,verbose){"+SENTINEL+" var on=!!i.conversationHad;"),
("(on?'Yes':'No')",
 "(on?(verbose?'Spoken':'Yes'):(verbose?'Not spoken':'No'))"),
("'<span class=\"iss-spoke\"><span class=\"iss-spoke-lbl\">Spoken</span>'+spokenToggle(i)+'</span></div>'",
 "'<span class=\"iss-spoke\">'+spokenToggle(i,true)+'</span></div>'"),
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
print("Applied PL_ISS_SPOKE_LABEL_V1. New size: %d bytes."%len(s.encode("utf-8")))
