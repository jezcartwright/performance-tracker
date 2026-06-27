import base64, sys
PATH="index.html"; SENTINEL="PL_PRI_NOLISTDEL_V1"
OLD=base64.b64decode('dmFyIGRlbD1jYW5FZGl0Pyc8YnV0dG9uIGNsYXNzPSJwcmktZGVsIiB0aXRsZT0iUmVtb3ZlIHByaW9yaXR5IiBvbmNsaWNrPSJwcmlEZWxldGUoXCcnK3AuaWQrJ1wnKSI+XHUyNzE1PC9idXR0b24+JzonJzs=').decode("utf-8")
NEW=base64.b64decode('dmFyIGRlbD0nJzsvKiBQTF9QUklfTk9MSVNUREVMX1YxICov').decode("utf-8")
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change.")
else:
    n=s.count(OLD)
    if n<1:
        sys.stderr.write("ABORT: anchor not found (count=%d)\n"%n); sys.exit(1)
    s=s.replace(OLD,NEW); open(PATH,"w",encoding="utf-8").write(s)
    print("Applied %s (%d card builder(s)). New size: %d bytes."%(SENTINEL,n,len(s.encode("utf-8"))))
