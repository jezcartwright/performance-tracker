import base64, sys
PATH="index.html"; SENTINEL="/* PL_ISS_LAYOUT_V1 */"
EDITS=[
("E1","K25vdGUrYWN0cm93K2lzc3VlUGVvcGxlSFRNTChpLGZhbHNlKSsnPC9kaXY+Jw==","K25vdGUrYWN0cm93Kyc8L2Rpdj4nKyc8ZGl2IGNsYXNzPSJpc3MtcGVvcGxlIj4nK2lzc3VlUGVvcGxlSFRNTChpLGZhbHNlKSsnPC9kaXY+Jw=="),
("E2a","Lmlzcy1jYXJke3Bvc2l0aW9uOnJlbGF0aXZlO2dyaWQtdGVtcGxhdGUtY29sdW1uczphdXRvIDFmciBhdXRvfQ==","Lmlzcy1jYXJke3Bvc2l0aW9uOnJlbGF0aXZlO2dyaWQtdGVtcGxhdGUtY29sdW1uczphdXRvIDFmciBhdXRvIGF1dG87YWxpZ24taXRlbXM6c3RhcnR9"),
("E2b","Lmlzcy1jYXJkIC5wcmktcmlnaHR7ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjthbGlnbi1pdGVtczpmbGV4LWVuZDtnYXA6NnB4fQ==","Lmlzcy1jYXJkIC5wcmktcmlnaHR7ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjthbGlnbi1pdGVtczpmbGV4LXN0YXJ0O2dhcDo2cHg7YWxpZ24tc2VsZjpzdHJldGNoO2JvcmRlci1sZWZ0OjFweCBzb2xpZCB2YXIoLS1iMik7cGFkZGluZy1sZWZ0OjE4cHh9"),
("E2c","Lndobzpob3Zlcj4ucG9wLC53aG8tYXY6aG92ZXI+LnBvcHtkaXNwbGF5OmJsb2NrfQ==","Lndobzpob3Zlcj4ucG9wLC53aG8tYXY6aG92ZXI+LnBvcHtkaXNwbGF5OmJsb2NrfQovKiBQTF9JU1NfTEFZT1VUX1YxICovCi5pc3MtcGVvcGxle2FsaWduLXNlbGY6c3RhcnR9Ci5pc3MtY2FyZCAucGItc20gLm1pbml7d2lkdGg6MjJweDtoZWlnaHQ6MjJweDtmb250LXNpemU6OXB4fQpAbWVkaWEobWF4LXdpZHRoOjU2MHB4KXsuaXNzLWNhcmR7Z3JpZC10ZW1wbGF0ZS1jb2x1bW5zOmF1dG8gMWZyO2dyaWQtdGVtcGxhdGUtYXJlYXM6bm9uZX0uaXNzLXBlb3BsZXtncmlkLWNvbHVtbjoxLy0xO21hcmdpbi10b3A6MTBweH0uaXNzLWNhcmQgLnByaS1yaWdodHtncmlkLWNvbHVtbjoxLy0xO2JvcmRlci1sZWZ0OjA7cGFkZGluZy1sZWZ0OjA7ZmxleC1kaXJlY3Rpb246cm93O2FsaWduLWl0ZW1zOmNlbnRlcjtnYXA6MTRweDttYXJnaW4tdG9wOjZweH19")
]
s=open(PATH,encoding="utf-8").read()
if SENTINEL in s:
    print("Already applied — no change."); sys.exit(0)
for tag,ob,nb in EDITS:
    old=base64.b64decode(ob).decode("utf-8"); new=base64.b64decode(nb).decode("utf-8")
    n=s.count(old)
    if n!=1:
        sys.stderr.write("ABORT %s: count=%d\n"%(tag,n)); sys.exit(1)
    s=s.replace(old,new); print("  %s ok"%tag)
open(PATH,"w",encoding="utf-8").write(s)
print("Applied PL_ISS_LAYOUT_V1. New size: %d bytes."%len(s.encode("utf-8")))
