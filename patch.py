import sys
PATH="index.html"; SENTINEL="/* PL_TOKENS_V1 */"
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change."); sys.exit(0)
anchor="--green:#0e9f6e;"
if s.count(anchor)!=1:
    sys.stderr.write("ABORT: :root anchor count=%d\n"%s.count(anchor)); sys.exit(1)
s=s.replace(anchor, anchor+SENTINEL, 1)
folds=[("#12936a","var(--green)",1),("#b42318","#e5252b",1),("#5a5550","var(--t2)",1)]
for src,dst,minn in folds:
    n=s.count(src)
    if n<minn:
        sys.stderr.write("ABORT: %s count=%d\n"%(src,n)); sys.exit(1)
    s=s.replace(src,dst); print("  %s -> %s  (%d)"%(src,dst,n))
open(PATH,"w",encoding="utf-8").write(s)
print("Applied PL_TOKENS_V1. New size: %d bytes."%len(s.encode("utf-8")))
