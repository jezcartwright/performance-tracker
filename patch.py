#!/usr/bin/env python3
# PL_CSSCOLOR_V1 — neutralise stored-XSS via colour values inserted into style="...".
# Strategy: one cssColor() allow-list sanitiser, applied where colour DATA enters
# the app (functions loader, company-theme loader) plus the member-writable issue
# colour (i.color). All downstream style="background:'+x+'" sites then render safe
# values. No render-site edits, landing srcdoc untouched.
import base64, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(PATH, encoding='utf-8').read()

SENT = 'function cssColor('
if SENT in s:
    print('ok already-applied (cssColor present) — no-op'); sys.exit(0)

def b(x): return base64.b64decode(x).decode('utf-8')

# ---- expected exact counts (measured on live source) --------------------------
EXPECT = {
 'fns[d.id]=Object.assign({id:d.id},d.data());': 1,
 'companies[d.id]=Object.assign({id:d.id},d.data());': 2,
 "var fc=i.color||(fns[i.functionId]&&fns[i.functionId].color)||'var(--strip)';": 3,
 "(i.color||'var(--strip)')": 1,
 'function personColor(mid){': 1,
}
for needle, n in EXPECT.items():
    got = s.count(needle)
    if got != n:
        print('ABORT anchor count %d!=%d for: %r' % (got, n, needle[:60])); sys.exit(1)

# ---- 1) cssColor() helper, inserted before personColor() ----------------------
HELPER = b(
 'ZnVuY3Rpb24gY3NzQ29sb3IoYyl7IGlmKGM9PW51bGwpcmV0dXJuICd2YXIoLS1zdHJpcCkn'
 'OyBjPVN0cmluZyhjKS50cmltKCk7IGlmKC9eI1swLTlhLWZBLUZdezMsOH0kLy50ZXN0KGMp'
 'KXJldHVybiBjOyBpZigvXnZhclwoLS1bYS16QS1aMC05LV0rXCkkLy50ZXN0KGMpKXJldHVy'
 'biBjOyBpZigvXihyZ2J8cmdiYXxoc2x8aHNsYSlcKFswLTkuLCVcL1xzXStcKSQvaS50ZXN0'
 'KGMpKXJldHVybiBjOyBpZigvXlthLXpBLVpdKyQvLnRlc3QoYykpcmV0dXJuIGM7IHJldHVy'
 'biAndmFyKC0tc3RyaXApJzsgfQo=')
anchor1 = 'function personColor(mid){'
s = s.replace(anchor1, HELPER + anchor1, 1)

# ---- 2) functions loader: sanitise .color ------------------------------------
old2 = 'fns[d.id]=Object.assign({id:d.id},d.data());'
new2 = ('var _fd=d.data(); if(_fd&&_fd.color!=null)_fd.color=cssColor(_fd.color); '
        'fns[d.id]=Object.assign({id:d.id},_fd);')
s = s.replace(old2, new2, 1)

# ---- 3) companies loader (x2): sanitise theme strip/ink/soft/mid -------------
old3 = 'companies[d.id]=Object.assign({id:d.id},d.data());'
new3 = (b("dmFyIF9jZD1kLmRhdGEoKTsgaWYoX2NkJiZfY2QudGhlbWUmJnR5cGVvZiBfY2QudGhlbWU9"
          "PT0nb2JqZWN0Jyl7WydzdHJpcCcsJ2luaycsJ3NvZnQnLCdtaWQnXS5mb3JFYWNoKGZ1bmN0"
          "aW9uKF9rKXtpZihfY2QudGhlbWVbX2tdIT1udWxsKV9jZC50aGVtZVtfa109Y3NzQ29sb3Io"
          "X2NkLnRoZW1lW19rXSk7fSk7fSA=")
        + 'companies[d.id]=Object.assign({id:d.id},_cd);')
cnt3 = s.count(old3)
if cnt3 != 2:
    print('ABORT companies count %d!=2' % cnt3); sys.exit(1)
s = s.replace(old3, new3)

# ---- 4) issue colour fc (x3): wrap in cssColor -------------------------------
old4 = "var fc=i.color||(fns[i.functionId]&&fns[i.functionId].color)||'var(--strip)';"
new4 = "var fc=cssColor(i.color||(fns[i.functionId]&&fns[i.functionId].color)||'var(--strip)');"
cnt4 = s.count(old4)
if cnt4 != 3:
    print('ABORT fc count %d!=3' % cnt4); sys.exit(1)
s = s.replace(old4, new4)

# ---- 5) lone (i.color||'var(--strip)') (x1) ----------------------------------
old5 = "(i.color||'var(--strip)')"
new5 = "cssColor(i.color||'var(--strip)')"
s = s.replace(old5, new5, 1)

# ---- post-conditions ---------------------------------------------------------
assert s.count('function cssColor(') == 1, 'helper not inserted'
assert s.count(new2) == 1, 'fns loader not patched'
assert s.count('companies[d.id]=Object.assign({id:d.id},_cd);') == 2, 'companies not patched'
assert s.count(new4) == 3, 'fc not patched'
assert s.count(old2) == 0 and s.count(old3) == 0 and s.count(old4) == 0, 'leftover originals'

open(PATH, 'w', encoding='utf-8').write(s)
print('ok cssColor helper inserted')
print('ok functions loader sanitised (1)')
print('ok companies theme loader sanitised (2)')
print('ok issue fc wrapped (3) + lone i.color (1)')
print('DONE')
