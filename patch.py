import base64, sys
PATH="index.html"; SENTINEL="color:#e5252b;font:600 13px/1 var(--ui)"
EDITS=[
('LnBkLWRlbHtiYWNrZ3JvdW5kOm5vbmU7Ym9yZGVyOjA7Y29sb3I6I2MwMzkyYjtmb250OjYwMCAxM3B4LzEgdmFyKC0tdWkpLHNhbnMtc2VyaWY7Y3Vyc29yOnBvaW50ZXI7cGFkZGluZzo4cHggMTJweDtib3JkZXItcmFkaXVzOjhweH0=','LnBkLWRlbHtiYWNrZ3JvdW5kOm5vbmU7Ym9yZGVyOjA7Y29sb3I6I2U1MjUyYjtmb250OjYwMCAxM3B4LzEgdmFyKC0tdWkpLHNhbnMtc2VyaWY7Y3Vyc29yOnBvaW50ZXI7cGFkZGluZzo4cHggMTJweDtib3JkZXItcmFkaXVzOjhweH0='),
('LnBkLWRlbDpob3ZlcntiYWNrZ3JvdW5kOiNmZGVjZWF9','LnBkLWRlbDpob3ZlcntiYWNrZ3JvdW5kOiNmZGYxZjB9')
]
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change.")
else:
    for k,(ob,nb) in enumerate(EDITS):
        old=base64.b64decode(ob).decode("utf-8"); new=base64.b64decode(nb).decode("utf-8")
        n=s.count(old)
        if n!=1:
            sys.stderr.write("ABORT edit %d: count=%d\n"%(k,n)); sys.exit(1)
        s=s.replace(old,new)
    open(PATH,"w",encoding="utf-8").write(s)
    print("Applied. New size: %d bytes."%len(s.encode("utf-8")))
