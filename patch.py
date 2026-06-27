import re, sys
PATH="index.html"; SENTINEL="/* PL_RADIUS_SCALE_V1 */"
MAP={5:8,6:8,7:8,9:8,10:12,11:12,13:12,14:12,18:16,20:16,30:16}
RX=re.compile(r'border-radius:\s*(\d+)px(?=\s*[;}"\'])')
def remap(t):
    return RX.sub(lambda m: 'border-radius:%dpx'%MAP.get(int(m.group(1)), int(m.group(1))), t)
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change.")
else:
    i=s.find('srcdoc="')+len('srcdoc="'); j=s.find('"', i)
    head, src, tail = s[:i], s[i:j], s[j:]
    s=remap(head)+src+remap(tail)
    anc="--green:#0e9f6e;"
    if s.count(anc)<1:
        sys.stderr.write("ABORT: :root anchor missing\n"); sys.exit(1)
    s=s.replace(anc, anc+SENTINEL, 1)
    open(PATH,"w",encoding="utf-8").write(s)
    print("Applied PL_RADIUS_SCALE_V1. New size: %d bytes."%len(s.encode("utf-8")))
