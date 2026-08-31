#!/usr/bin/env python3
from pathlib import Path

TITLE_OLD = """  if (_rt) {
    if (recKey === 'incomplete') _rt.textContent = 'Profile incomplete';
    else _rt.textContent = recName;
  }
  if (_rs) {
    if (recKey === 'incomplete') _rs.textContent = 'Finish remaining first-pass items.';
    else _rs.textContent = recLine;
  }"""

TITLE_NEW = """  const _rlbl = document.querySelector('#resJump .lbl');
  if (_rlbl) _rlbl.textContent = recKey === 'incomplete' ? 'Results' : 'Comparison';
  if (_rt) {
    if (recKey === 'incomplete') _rt.textContent = 'Profile incomplete';
    else if (d.primary === 'bsc') _rt.textContent = 'Outside Phase III IO populations';
    else if (d.primary === 'tki') _rt.textContent = 'IO pathway needs individual discussion';
    else if (ds.dual) _rt.textContent = 'A+B and STRIDE both discussable';
    else _rt.textContent = 'Trial design comparison';
  }
  if (_rs) {
    if (recKey === 'incomplete') _rs.textContent = 'Finish remaining first-pass items.';
    else _rs.textContent = 'Closest enrolled-like design among IMbrave150, HIMALAYA + SIERRA, and CheckMate 9DW. Not a prescription and not an OS rank.';
  }"""

HTML_OLD_A = """  const htmlOut = recLead +
    `<details class=\"mdt-fold\" id=\"res-details\"><summary>Details</summary><div class=\"fold-body\">${matchLead}${designLead}"""

HTML_OLD_B = """  const htmlOut = recLead +
    `<details class=\"mdt-fold\" id=\"res-details\"><summary>Details</summary><div class=\"fold-body\">${designLead}"""

HTML_OLD_C = """  const htmlOut = matchLead + recLead +
    `<details class=\"mdt-fold\" id=\"res-details\"><summary>Details</summary><div class=\"fold-body\">${designLead}"""

HTML_NEW = """  const htmlOut = matchLead +
    `<details class=\"mdt-fold\" id=\"res-details\"><summary>Details</summary><div class=\"fold-body\">${recLead}${designLead}"""

def patch(s):
    n = 0
    if TITLE_OLD in s:
        s = s.replace(TITLE_OLD, TITLE_NEW, 1)
        n += 1
    for old in (HTML_OLD_A, HTML_OLD_B, HTML_OLD_C):
        if old in s:
            s = s.replace(old, HTML_NEW, 1)
            n += 1
            break
    if '<div class="lbl">Recommendation</div>' in s:
        s = s.replace('<div class="lbl">Recommendation</div>', '<div class="lbl">Comparison</div>', 1)
        n += 1
    return s, n

def main():
    for name in ('index.html', 'hcc-simulator.html'):
        p = Path(name)
        if not p.exists():
            print('skip', name)
            continue
        raw = p.read_text(encoding='utf-8')
        out, n = patch(raw)
        if out != raw:
            p.write_text(out, encoding='utf-8')
        print(name, 'repl', n)
        assert 'Trial design comparison' in out
        assert 'function decide()' in out
        assert 'else _rt.textContent = recName;' not in out

if __name__ == '__main__':
    main()
