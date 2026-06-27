#!/usr/bin/env python3
# PL_PRI_DELETE_V1 — delete a priority + fix the tall empty gap on the detail view.
#  - CSS: #priDetail .chat kept the base .chat fixed height:548px (only display
#    was overridden), leaving a big empty box under the progress composer. Now
#    height:auto with a bounded, scrollable log. Adds delete-button styles.
#  - Markup: a "Delete priority" action at the foot of the detail card.
#  - JS: deletePriority() removes the open priority (owner/admin per rules) and
#    returns to My Priorities.
# App-only; idempotent.
import base64, sys
PATH="index.html"; SENTINEL="PL_PRI_DELETE_V1"
EDITS=[
('I3ByaURldGFpbCAuY2hhdHtkaXNwbGF5OmJsb2NrfQojcHJpRGV0YWlsIC5tc2dze21pbi1oZWlnaHQ6MTIwcHh9','I3ByaURldGFpbCAuY2hhdHtkaXNwbGF5OmJsb2NrO2hlaWdodDphdXRvfQojcHJpRGV0YWlsIC5tc2dze21pbi1oZWlnaHQ6OTZweDttYXgtaGVpZ2h0OjQyMHB4fQoucGQtZm9vdHttYXJnaW4tdG9wOjE4cHg7cGFkZGluZy10b3A6MTRweDtib3JkZXItdG9wOjFweCBzb2xpZCB2YXIoLS1iKTt0ZXh0LWFsaWduOmNlbnRlcn0KLnBkLWRlbHtiYWNrZ3JvdW5kOm5vbmU7Ym9yZGVyOjA7Y29sb3I6I2MwMzkyYjtmb250OjYwMCAxM3B4LzEgdmFyKC0tdWkpLHNhbnMtc2VyaWY7Y3Vyc29yOnBvaW50ZXI7cGFkZGluZzo4cHggMTJweDtib3JkZXItcmFkaXVzOjhweH0KLnBkLWRlbDpob3ZlcntiYWNrZ3JvdW5kOiNmZGVjZWF9'),
('PHBhdGggZD0iTTIyIDIgMTEgMTMiLz48L3N2Zz48L2J1dHRvbj4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KPC9zZWN0aW9uPgogIDxzZWN0aW9uIGNsYXNzPSJzY3JlZW4iIGlkPSJyYWlzZVByaW9yaXR5Ij4=','PHBhdGggZD0iTTIyIDIgMTEgMTMiLz48L3N2Zz48L2J1dHRvbj4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0icGQtZm9vdCI+PGJ1dHRvbiB0eXBlPSJidXR0b24iIGNsYXNzPSJwZC1kZWwiIG9uY2xpY2s9ImRlbGV0ZVByaW9yaXR5KCkiPkRlbGV0ZSBwcmlvcml0eTwvYnV0dG9uPjwvZGl2PgogIDwvZGl2Pgo8L3NlY3Rpb24+CiAgPHNlY3Rpb24gY2xhc3M9InNjcmVlbiIgaWQ9InJhaXNlUHJpb3JpdHkiPg=='),
('dmFyIGN1clBpZD1udWxsLCBjdXJQcmk9bnVsbCwgc3ViUE09bnVsbDs=','dmFyIGN1clBpZD1udWxsLCBjdXJQcmk9bnVsbCwgc3ViUE09bnVsbDsKLyogUExfUFJJX0RFTEVURV9WMSAqLwp3aW5kb3cuZGVsZXRlUHJpb3JpdHk9ZnVuY3Rpb24oKXsgdmFyIGlkPWN1clBpZHx8KGN1clByaSYmY3VyUHJpLmlkKTsgaWYoIWlkKXJldHVybjsgaWYoIWNvbmZpcm0oJ0RlbGV0ZSB0aGlzIHByaW9yaXR5PyBUaGlzIGNhbm5vdCBiZSB1bmRvbmUuJykpcmV0dXJuOyBwcmlvcml0aWVzUmVmKCkuZG9jKGlkKS5kZWxldGUoKS50aGVuKGZ1bmN0aW9uKCl7IGdvUHJpb3JpdGllcygpOyB9KS5jYXRjaChmdW5jdGlvbihlKXsgYWxlcnQoJ0NvdWxkIG5vdCBkZWxldGU6ICcrKChlJiZlLm1lc3NhZ2UpfHxlKSk7IH0pOyB9Ow==')
]
def main():
    s=open(PATH,encoding="utf-8").read()
    if SENTINEL in s:
        print("Already applied (%s present) — no change."%SENTINEL); return
    for k,(ob,nb) in enumerate(EDITS):
        old=base64.b64decode(ob).decode("utf-8"); new=base64.b64decode(nb).decode("utf-8")
        n=s.count(old)
        if n!=1:
            sys.stderr.write("ABORT edit %d: anchor count=%d (expected 1)\n"%(k,n)); sys.exit(1)
        s=s.replace(old,new)
    open(PATH,"w",encoding="utf-8").write(s)
    print("Applied %s. New size: %d bytes."%(SENTINEL,len(s.encode("utf-8"))))
if __name__=="__main__": main()
