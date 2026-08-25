#!/usr/bin/env python3
# PT_NODEPT_V1 — department is optional when adding/editing a person: adds a default "No department" option
# and lets save store functionId=null (no forced department naming). Idempotent.
import sys, base64
SENT="value=\"__none\""
PAIRS=[('ZnVuY3Rpb24gcmVuZGVyUHNEZXB0KHNlbCl7IHZhciBzPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdwcy1kZXB0Jyk7IHZhciBvcHRzPScnOwogIE9iamVjdC5rZXlzKGZucykuZm9yRWFjaCg=', 'ZnVuY3Rpb24gcmVuZGVyUHNEZXB0KHNlbCl7IHZhciBzPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdwcy1kZXB0Jyk7IHZhciBvcHRzPScnOwogIG9wdHMrPSc8b3B0aW9uIHZhbHVlPSJfX25vbmUiJysoKCFmbnNbc2VsXSAmJiBzZWwhPT0nX19uZXcnKT8nIHNlbGVjdGVkJzonJykrJz5ObyBkZXBhcnRtZW50PC9vcHRpb24+JzsKICBPYmplY3Qua2V5cyhmbnMpLmZvckVhY2go'), ('ICBvcHRzKz0nPG9wdGlvbiB2YWx1ZT0iX19uZXciJysoIU9iamVjdC5rZXlzKGZucykubGVuZ3RoPycgc2VsZWN0ZWQnOicnKSsnPuKelSBOZXcgZGVwYXJ0bWVudOKApjwvb3B0aW9uPic7', 'ICBvcHRzKz0nPG9wdGlvbiB2YWx1ZT0iX19uZXciPuKelSBOZXcgZGVwYXJ0bWVudOKApjwvb3B0aW9uPic7'), ('ICB2YXIgZW5zdXJlPShkdj09PSdfX25ldycpP2NyZWF0ZURlcHRJbmxpbmUobmV3RGVwdE5tKTpQcm9taXNlLnJlc29sdmUoZHYpOwogIGVuc3VyZS50aGVuKGZ1bmN0aW9uKGZpZCl7IGlmKCFmaWQpIHRocm93IG5ldyBFcnJvcignUGxlYXNlIG5hbWUgdGhlIGRlcGFydG1lbnQuJyk7', 'ICB2YXIgZW5zdXJlPShkdj09PSdfX25ldycpP2NyZWF0ZURlcHRJbmxpbmUobmV3RGVwdE5tKTpQcm9taXNlLnJlc29sdmUoZHY9PT0nX19ub25lJz9udWxsOmR2KTsKICBlbnN1cmUudGhlbihmdW5jdGlvbihmaWQpeyBpZihkdj09PSdfX25ldycgJiYgIWZpZCkgdGhyb3cgbmV3IEVycm9yKCdQbGVhc2UgbmFtZSB0aGUgZGVwYXJ0bWVudC4nKTs=')]
def d64(s): return base64.b64decode(s).decode("utf-8")
def main():
    if len(sys.argv)<2: sys.exit("usage: python3 build_nodept_patch.py index.html")
    p=sys.argv[1]; d=open(p,encoding="utf-8").read()
    if 'value="__none"' in d: print("PT_NODEPT_V1 already present — no-op."); return
    for i,(eo,en) in enumerate(PAIRS):
        o=d64(eo); n=d64(en); c=d.count(o)
        if c!=1: sys.exit("ABORT: hunk %d anchor count %d (expected 1)"%(i,c))
        d=d.replace(o,n,1)
    open(p,"w",encoding="utf-8").write(d); print("PT_NODEPT_V1 applied OK (3 hunks).")
main()
