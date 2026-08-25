#!/usr/bin/env python3
# PT_FREELIST_V1 — make the org "By reporting line" list use the free-form tree (freeChildren) so no-dept
# people appear and it matches the chart; also make freeParent ignore hidden coach managers. Idempotent.
import sys, base64
SENT="var kids=freeChildren(mid);"
PAIRS=[('ICBpZihtZyAmJiBtZyE9PW1pZCAmJiBtZW1iZXJzW21nXSkgcmV0dXJuIG1nOw==', 'ICBpZihtZyAmJiBtZyE9PW1pZCAmJiBtZW1iZXJzW21nXSAmJiAhb3JnSGlkZGVuKG1nKSkgcmV0dXJuIG1nOw=='), ('ZnVuY3Rpb24gb2xOb2RlKG1pZCxkZXB0aCxzZWVuKXsgc2Vlbj1zZWVufHx7fTsgaWYoc2VlblttaWRdKXJldHVybiAnJzsgc2VlblttaWRdPTE7CiAgdmFyIGtpZHM9c2libGluZ3NVbmRlcihtaWQpOw==', 'ZnVuY3Rpb24gb2xOb2RlKG1pZCxkZXB0aCxzZWVuKXsgc2Vlbj1zZWVufHx7fTsgaWYoc2VlblttaWRdKXJldHVybiAnJzsgc2VlblttaWRdPTE7CiAgdmFyIGtpZHM9ZnJlZUNoaWxkcmVuKG1pZCk7'), ('ZnVuY3Rpb24gb3JnTGlzdExpbmUoKXsKICB2YXIgY2VvPWNvbXBhbnkuY2VvTWVtYmVySWQ7CiAgaWYoY2VvJiZtZW1iZXJzW2Nlb10pIHJldHVybiBvbE5vZGUoY2VvLDApOwogIHZhciByb290cz1kZXB0TGlzdCgpLm1hcChmbnNMZWFkZXIpLmZpbHRlcihmdW5jdGlvbih4KXtyZXR1cm4geCYmbWVtYmVyc1t4XTt9KTsKICBpZighcm9vdHMubGVuZ3RoKSByZXR1cm4gJzxkaXYgY2xhc3M9Im9sLWVtcHR5Ij5ObyBwZW9wbGUgeWV0LjwvZGl2Pic7CiAgcmV0dXJuIHJvb3RzLm1hcChmdW5jdGlvbihsKXtyZXR1cm4gb2xOb2RlKGwsMCk7fSkuam9pbignJyk7Cn0=', 'ZnVuY3Rpb24gb3JnTGlzdExpbmUoKXsKICB2YXIgY2VvPWNvbXBhbnkuY2VvTWVtYmVySWQ7IHZhciBzZWVuPXt9OyB2YXIgaHRtbD0nJzsKICBpZihjZW8mJm1lbWJlcnNbY2VvXSl7IGh0bWw9b2xOb2RlKGNlbywwLHNlZW4pOyB9CiAgZWxzZSB7IHZhciByb290cz1PYmplY3Qua2V5cyhtZW1iZXJzKS5maWx0ZXIoZnVuY3Rpb24oeCl7cmV0dXJuICFvcmdIaWRkZW4oeCkmJiFmcmVlUGFyZW50KHgpO30pLnNvcnQoZnVuY3Rpb24oYSxiKXtyZXR1cm4gb3JkT2YoYSktb3JkT2YoYik7fSk7IGh0bWw9cm9vdHMubWFwKGZ1bmN0aW9uKGwpe3JldHVybiBvbE5vZGUobCwwLHNlZW4pO30pLmpvaW4oJycpOyB9CiAgaHRtbCs9T2JqZWN0LmtleXMobWVtYmVycykuZmlsdGVyKGZ1bmN0aW9uKHgpe3JldHVybiAhc2Vlblt4XSYmIW9yZ0hpZGRlbih4KTt9KS5zb3J0KGZ1bmN0aW9uKGEsYil7cmV0dXJuIG9yZE9mKGEpLW9yZE9mKGIpO30pLm1hcChmdW5jdGlvbih4KXtyZXR1cm4gb2xOb2RlKHgsMCxzZWVuKTt9KS5qb2luKCcnKTsKICByZXR1cm4gaHRtbHx8JzxkaXYgY2xhc3M9Im9sLWVtcHR5Ij5ObyBwZW9wbGUgeWV0LjwvZGl2Pic7Cn0=')]
def d64(s): return base64.b64decode(s).decode("utf-8")
def main():
    if len(sys.argv)<2: sys.exit("usage: python3 build_freelist_patch.py index.html")
    p=sys.argv[1]; d=open(p,encoding="utf-8").read()
    if SENT in d: print("PT_FREELIST_V1 already present — no-op."); return
    for i,(eo,en) in enumerate(PAIRS):
        o=d64(eo); n=d64(en); c=d.count(o)
        if c!=1: sys.exit("ABORT: hunk %d anchor count %d (expected 1)"%(i,c))
        d=d.replace(o,n,1)
    open(p,"w",encoding="utf-8").write(d); print("PT_FREELIST_V1 applied OK (3 hunks).")
main()
