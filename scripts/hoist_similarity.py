#!/usr/bin/env python3
from pathlib import Path

def hoist(text: str) -> str:
    old_toc = '''  const toc = `<nav class="res-toc" aria-label="Results sections">
    <a href="#sec-design">Study design</a>
    <a href="#sec-efficacy">Efficacy</a>
    <a href="#sec-match">Trial similarity</a>'''
    new_toc = '''  const toc = `<nav class="res-toc" aria-label="Results sections">
    <a href="#sec-match">Trial similarity</a>
    <a href="#sec-design">Study design</a>
    <a href="#sec-efficacy">Efficacy</a>'''
    if old_toc in text:
        text = text.replace(old_toc, new_toc, 1)
    old_out = '  const htmlOut = recLead +'
    new_out = '  const htmlOut = matchLead + recLead +'
    if old_out in text and 'const htmlOut = matchLead + recLead +' not in text:
        text = text.replace(old_out, new_out, 1)
    old_mark = '  detailInner += `<div class="tier preferred" id="sec-match">'
    new_mark = '  const matchLead = rankedCards.length ? `<div class="tier preferred" id="sec-match">'
    if old_mark in text:
        text = text.replace(old_mark, new_mark, 1)
        text = text.replace(
            '    </div>\n  </div>`;\n  detailInner += mdtFold(\'fold-break\'',
            '    </div>\n  </div>` : \'\';\n  detailInner += mdtFold(\'fold-break\'',
            1
        )
    old_css = (
        'body.view-results .res-banner { margin-bottom: 16px !important; padding-bottom: 16px !important; }\n'
        'body.view-results #res-details > summary {'
    )
    new_css = (
        'body.view-results .res-banner { margin-bottom: 16px !important; padding-bottom: 16px !important; }\n'
        'body.view-results #sec-match { margin: 8px 0 24px !important; }\n'
        'body.view-results #sec-match .tier-head {\n'
        '  display: flex !important;\n'
        '  align-items: baseline;\n'
        '  justify-content: space-between;\n'
        '  gap: 12px;\n'
        '  margin: 0 0 10px !important;\n'
        '}\n'
        'body.view-results #sec-match .sim-big { margin: 0 0 8px !important; }\n'
        'body.view-results #res-details > summary {'
    )
    if old_css in text:
        text = text.replace(old_css, new_css, 1)
    return text

if __name__ == '__main__':
    for name in ('index.html', 'hcc-simulator.html'):
        p = Path(name)
        if not p.exists():
            print(name, 'missing')
            continue
        t = p.read_text(encoding='utf-8')
        n = hoist(t)
        if n == t:
            print(name, 'no changes', p.stat().st_size)
        else:
            p.write_text(n, encoding='utf-8')
            print(name, 'patched', p.stat().st_size)
