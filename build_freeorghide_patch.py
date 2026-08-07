#!/usr/bin/env python3
# PT_FREEORGHIDE_V1 — keep the super-admin/coach seat out of the free-form org chart (it was never drawn
# before; it is shown via the coach card and excluded from counts). Excludes m.coach / super email. Idempotent.
import sys, base64
SENT="function orgHidden("
PAIRS=[('ZnVuY3Rpb24gZnJlZVBhcmVudChtaWQpew==', 'ZnVuY3Rpb24gb3JnSGlkZGVuKG1pZCl7IHZhciBtPW1lbWJlcnNbbWlkXTsgaWYoIW0pcmV0dXJuIGZhbHNlOyBpZihtLmNvYWNoKXJldHVybiB0cnVlOyBpZihtLmVtYWlsICYmIHR5cGVvZiBTVVBFUl9BRE1JTl9FTUFJTFMhPT0ndW5kZWZpbmVkJyAmJiBTVVBFUl9BRE1JTl9FTUFJTFMuaW5kZXhPZigobS5lbWFpbHx8JycpLnRvTG93ZXJDYXNlKCkpPj0wKXJldHVybiB0cnVlOyByZXR1cm4gZmFsc2U7IH0KZnVuY3Rpb24gZnJlZVBhcmVudChtaWQpew=='), ('cmV0dXJuIE9iamVjdC5rZXlzKG1lbWJlcnMpLmZpbHRlcihmdW5jdGlvbih4KXsgcmV0dXJuIHghPT1taWQgJiYgZnJlZVBhcmVudCh4KT09PW1pZDsgfSk=', 'cmV0dXJuIE9iamVjdC5rZXlzKG1lbWJlcnMpLmZpbHRlcihmdW5jdGlvbih4KXsgcmV0dXJuIHghPT1taWQgJiYgIW9yZ0hpZGRlbih4KSAmJiBmcmVlUGFyZW50KHgpPT09bWlkOyB9KQ=='), ('T2JqZWN0LmtleXMobWVtYmVycykuZm9yRWFjaChmdW5jdGlvbih4KXsgaWYobWVtYmVyc1t4XS5mdW5jdGlvbklkPT09Rk9DVVNGSUQpIGluU2V0W3hdPTE7IH0pOw==', 'T2JqZWN0LmtleXMobWVtYmVycykuZm9yRWFjaChmdW5jdGlvbih4KXsgaWYobWVtYmVyc1t4XS5mdW5jdGlvbklkPT09Rk9DVVNGSUQgJiYgIW9yZ0hpZGRlbih4KSkgaW5TZXRbeF09MTsgfSk7'), ('dmFyIGV4dHJhPU9iamVjdC5rZXlzKG1lbWJlcnMpLmZpbHRlcihmdW5jdGlvbih4KXtyZXR1cm4gIXNlZW5beF07fSk=', 'dmFyIGV4dHJhPU9iamVjdC5rZXlzKG1lbWJlcnMpLmZpbHRlcihmdW5jdGlvbih4KXtyZXR1cm4gIXNlZW5beF0gJiYgIW9yZ0hpZGRlbih4KTt9KQ=='), ('LmpvaW4oJycpK09iamVjdC5rZXlzKG1lbWJlcnMpLmZpbHRlcihmdW5jdGlvbih4KXtyZXR1cm4gIXNlZW5beF07fSkubWFwKGZ1bmN0aW9uKHgpe3JldHVybiBmcmVlTm9kZSh4LHNlZW4pO30p', 'LmpvaW4oJycpK09iamVjdC5rZXlzKG1lbWJlcnMpLmZpbHRlcihmdW5jdGlvbih4KXtyZXR1cm4gIXNlZW5beF0gJiYgIW9yZ0hpZGRlbih4KTt9KS5tYXAoZnVuY3Rpb24oeCl7cmV0dXJuIGZyZWVOb2RlKHgsc2Vlbik7fSk='), ('dmFyIHJvb3RzMj1PYmplY3Qua2V5cyhtZW1iZXJzKS5maWx0ZXIoZnVuY3Rpb24oeCl7cmV0dXJuICFmcmVlUGFyZW50KHgpO30p', 'dmFyIHJvb3RzMj1PYmplY3Qua2V5cyhtZW1iZXJzKS5maWx0ZXIoZnVuY3Rpb24oeCl7cmV0dXJuICFvcmdIaWRkZW4oeCkgJiYgIWZyZWVQYXJlbnQoeCk7fSk=')]
def d64(s): return base64.b64decode(s).decode("utf-8")
def main():
    if len(sys.argv)<2: sys.exit("usage: python3 build_freeorghide_patch.py index.html")
    p=sys.argv[1]; d=open(p,encoding="utf-8").read()
    if SENT in d: print("PT_FREEORGHIDE_V1 already present — no-op."); return
    for i,(eo,en) in enumerate(PAIRS):
        o=d64(eo); n=d64(en); c=d.count(o)
        if c!=1: sys.exit("ABORT: hunk %d anchor count %d (expected 1)"%(i,c))
        d=d.replace(o,n,1)
    open(p,"w",encoding="utf-8").write(d); print("PT_FREEORGHIDE_V1 applied OK (6 hunks).")
main()
