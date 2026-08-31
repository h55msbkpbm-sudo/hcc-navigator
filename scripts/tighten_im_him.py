#!/usr/bin/env python3
from pathlib import Path

REPLACES = [
    (
        "if (A.varices === 'none') { im = 7; him = 3; cm = 1; detail = 'no varices'; }",
        "if (A.varices === 'none') { im = 7; him = 5; cm = 2; detail = 'no varices'; }",
    ),
    (
        "if (A.egd === 'yes' && A.varices === 'none') { im = 6; him = 3; cm = 1; detail = 'EGD feasible, no varices'; }",
        "if (A.egd === 'yes' && A.varices === 'none') { im = 6; him = 5; cm = 2; detail = 'EGD feasible, no varices'; }",
    ),
    (
        "if (A.cardio === 'low') { im = 6; him = 3; cm = 1; detail = 'low CV risk'; }",
        "if (A.cardio === 'low') { im = 6; him = 5; cm = 2; detail = 'low CV risk'; }",
    ),
    (
        "else if (open) { himD = 6; himNote = 'STRIDE eligible; IMbrave design still closer when anti-VEGF fully open'; }",
        "else if (open) { himD = 9; himNote = 'STRIDE remains a first-line design when anti-VEGF is open; IMbrave is slightly closer'; }",
    ),
]

STRETCH_OLD = """    const factor = near ? 1.0 : (span < 12 ? 1.85 : (span < 20 ? 1.5 : (span < 30 ? 1.28 : 1.12)));
    raw.forEach(x => {
      const stretched = mean + (x.p - mean) * factor;
      spread[x.t === imbrave ? 'im' : x.t === himalaya ? 'him' : 'cm'] =
        Math.round(Math.max(8, Math.min(96, stretched)));
    });"""

STRETCH_NEW = """    const factor = near ? 1.0 : (span < 12 ? 1.15 : 1.0);
    raw.forEach(x => {
      const key = x.t === imbrave ? 'im' : x.t === himalaya ? 'him' : 'cm';
      if (key !== 'cm') {
        spread[key] = x.p;
        return;
      }
      const stretched = mean + (x.p - mean) * factor;
      spread[key] = Math.round(Math.max(8, Math.min(96, stretched)));
    });"""

def patch(s):
    n = 0
    for a, b in REPLACES:
        if a in s:
            s = s.replace(a, b, 1)
            n += 1
    if STRETCH_OLD in s:
        s = s.replace(STRETCH_OLD, STRETCH_NEW, 1)
        n += 1
    return s, n

def main():
    for name in ("index.html", "hcc-simulator.html"):
        p = Path(name)
        if not p.exists():
            print("skip", name)
            continue
        raw = p.read_text(encoding="utf-8")
        out, n = patch(raw)
        if n:
            p.write_text(out, encoding="utf-8")
            print("patched", name, "replacements", n)
        else:
            print("no change", name)

if __name__ == "__main__":
    main()
