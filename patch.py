import base64, sys
PATH="index.html"; SENTINEL="PL_TAGOTHERS_STAYOPEN_V1"
OLD=base64.b64decode("d2luZG93LmFkZFBpY2s9ZnVuY3Rpb24obSl7IGlmKG0hPT1NRS5taWQgJiYgcmlPdGhlcnMuaW5kZXhPZihtKTwwKXsgcmlPdGhlcnMucHVzaChtKTsgcmVuZGVyQ2hpcHMoKTsgfSB2YXIgaW5wPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyaS1hZGQtaW5wdXQnKTsgaWYoaW5wKWlucC52YWx1ZT0nJzsgaGlkZVRhKCdyaS1hZGQtbGlzdCcpOyB9Ow==").decode("utf-8")
NEW=base64.b64decode("d2luZG93LmFkZFBpY2s9ZnVuY3Rpb24obSl7IGlmKG0hPT1NRS5taWQgJiYgcmlPdGhlcnMuaW5kZXhPZihtKTwwKXsgcmlPdGhlcnMucHVzaChtKTsgcmVuZGVyQ2hpcHMoKTsgfSB2YXIgaW5wPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyaS1hZGQtaW5wdXQnKTsgaWYoaW5wKXsgaW5wLnZhbHVlPScnOyBpbnAuZm9jdXMoKTsgfSByZW5kZXJUYUxpc3QoJ3JpLWFkZC1saXN0JywgJycsIHJpT3RoZXJzLmNvbmNhdChbTUUubWlkXSksICdhZGRQaWNrJyk7IH07LyogUExfVEFHT1RIRVJTX1NUQVlPUEVOX1YxICov").decode("utf-8")
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change.")
else:
    n=s.count(OLD)
    if n!=1:
        sys.stderr.write("ABORT: anchor count=%d (expected 1)\n"%n); sys.exit(1)
    s=s.replace(OLD,NEW); open(PATH,"w",encoding="utf-8").write(s)
    print("Applied %s. New size: %d bytes."%(SENTINEL,len(s.encode("utf-8"))))
