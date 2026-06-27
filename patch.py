import sys
PATH="index.html"; SENTINEL="/* PL_ISS_LAYOUT_FIX_V1 */"
EDITS=[
(".iss-card{position:relative;grid-template-columns:auto 1fr auto auto;align-items:start}",
 ".pri-card.iss-card{position:relative;grid-template-columns:auto 1fr auto auto;align-items:start}"+SENTINEL),
("@media(max-width:560px){.iss-card{grid-template-columns:auto 1fr;grid-template-areas:none}",
 "@media(max-width:560px){.pri-card.iss-card{grid-template-columns:auto 1fr;grid-template-areas:none}"),
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
print("Applied PL_ISS_LAYOUT_FIX_V1. New size: %d bytes."%len(s.encode("utf-8")))
