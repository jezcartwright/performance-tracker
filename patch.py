import base64, sys
PATH="index.html"; SENTINEL="border-radius:6px;height:38px;padding:0 12px;font-family:var(--ui)"
EDITS=[
('LmNvLXN3aXRjaHtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2JvcmRlcjoxcHggc29saWQgdmFyKC0tYik7Ym9yZGVyLXJhZGl1czo2cHg7cGFkZGluZzo4cHggMTFweDtmb250LWZhbWlseTp2YXIoLS11aSk7Zm9udC1zaXplOjEzcHg7Zm9udC13ZWlnaHQ6NzAwO2NvbG9yOnZhcigtLXQyKTtiYWNrZ3JvdW5kOnZhcigtLWNhcmQpO2N1cnNvcjpwb2ludGVyO21heC13aWR0aDoyMDBweH0=','LmNvLXN3aXRjaHtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2JvcmRlcjoxcHggc29saWQgdmFyKC0tYik7Ym9yZGVyLXJhZGl1czo2cHg7aGVpZ2h0OjM4cHg7cGFkZGluZzowIDEycHg7Zm9udC1mYW1pbHk6dmFyKC0tdWkpO2ZvbnQtc2l6ZToxM3B4O2ZvbnQtd2VpZ2h0OjcwMDtjb2xvcjp2YXIoLS10Mik7YmFja2dyb3VuZDp2YXIoLS1jYXJkKTtjdXJzb3I6cG9pbnRlcjttYXgtd2lkdGg6MjAwcHh9'),
('LnVzZXJwaWxse2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50ZXI7Z2FwOjhweDtiYWNrZ3JvdW5kOnZhcigtLWNhcmQpO2JvcmRlcjoxcHggc29saWQgdmFyKC0tYik7Ym9yZGVyLXJhZGl1czo3cHg7cGFkZGluZzo0cHggMTFweCA0cHggNHB4O2ZvbnQtd2VpZ2h0OjYwMDtmb250LXNpemU6MTNweH0=','LnVzZXJwaWxse2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50ZXI7Z2FwOjhweDtiYWNrZ3JvdW5kOnZhcigtLWNhcmQpO2JvcmRlcjoxcHggc29saWQgdmFyKC0tYik7Ym9yZGVyLXJhZGl1czo2cHg7aGVpZ2h0OjM4cHg7cGFkZGluZzowIDExcHggMCA0cHg7Zm9udC13ZWlnaHQ6NjAwO2ZvbnQtc2l6ZToxM3B4fQ==')
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
