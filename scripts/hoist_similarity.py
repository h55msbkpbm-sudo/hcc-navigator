#!/usr/bin/env python3
"""Hoist trial baseline similarity cards to the top of Results and keep Results visible on ?view=results."""
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
    new_mark = '  const matchLead = rankedCards.length ? `<div class="match-lead" id="sec-match">'
    if old_mark in text:
        text = text.replace(old_mark, new_mark, 1)
        text = text.replace(
            "    </div>\n  </div>`;\n  detailInner += mdtFold('fold-break'",
            "    </div>\n  </div>` : '';\n  detailInner += mdtFold('fold-break'",
            1
        )

    text = text.replace(
        'const matchLead = rankedCards.length ? `<div class="tier preferred" id="sec-match">',
        'const matchLead = rankedCards.length ? `<div class="match-lead" id="sec-match">',
        1
    )

    old_css = (
        'body.view-results #sec-match { margin: 8px 0 24px !important; }\n'
        'body.view-results #sec-match .tier-head {\n'
        '  display: flex !important;\n'
        '  align-items: baseline;\n'
        '  justify-content: space-between;\n'
        '  gap: 12px;\n'
        '  margin: 0 0 10px !important;\n'
        '}\n'
        'body.view-results #sec-match .sim-big { margin: 0 0 8px !important; }\n'
    )
    new_css = (
        'body.view-results #sec-match,\n'
        'body.view-results .match-lead {\n'
        '  display: block !important;\n'
        '  margin: 4px 0 24px !important;\n'
        '  padding: 16px 18px 14px !important;\n'
        '  background: #fff !important;\n'
        '  border: 1px solid #d8d2c8 !important;\n'
        '  border-radius: 2px !important;\n'
        '  box-shadow: none !important;\n'
        '}\n'
        'body.view-results #sec-match .tier-head,\n'
        'body.view-results .match-lead .tier-head {\n'
        '  display: flex !important;\n'
        '  align-items: baseline;\n'
        '  justify-content: space-between;\n'
        '  gap: 12px;\n'
        '  margin: 0 0 12px !important;\n'
        '  background: transparent !important;\n'
        '}\n'
        'body.view-results #sec-match .sim-big,\n'
        'body.view-results .match-lead .sim-big {\n'
        '  margin: 0 0 8px !important;\n'
        '}\n'
    )
    if old_css in text:
        text = text.replace(old_css, new_css, 1)
    elif 'body.view-results .match-lead {' not in text:
        needle = 'body.view-results .res-banner { margin-bottom: 16px !important; padding-bottom: 16px !important; }\n'
        if needle in text:
            text = text.replace(needle, needle + new_css, 1)

    old_init = (
        '  let fromQuery = false;\n'
        '  try {\n'
        '    const params = new URLSearchParams(location.search);\n'
        '    if ([...params.keys()].some(function(k) { return k !== \'embed\' && k !== \'view\'; })) {\n'
        '      fromQuery = applyQueryProfile(params);\n'
        '      if (fromQuery && params.get(\'view\') === \'results\') {\n'
        '        showRec(false);\n'
        '      }\n'
        '    }\n'
        '  } catch (e) {}\n'
    )
    new_init = (
        '  let fromQuery = false;\n'
        '  let wantResults = false;\n'
        '  try {\n'
        '    const params = new URLSearchParams(location.search);\n'
        '    if ([...params.keys()].some(function(k) { return k !== \'embed\' && k !== \'view\'; })) {\n'
        '      fromQuery = applyQueryProfile(params);\n'
        '      if (fromQuery && params.get(\'view\') === \'results\') {\n'
        '        wantResults = true;\n'
        '        showRec(false);\n'
        '      }\n'
        '    } else if (params.get(\'view\') === \'results\') {\n'
        '      wantResults = true;\n'
        '      showRec(false);\n'
        '    }\n'
        '  } catch (e) {}\n'
    )
    if old_init in text:
        text = text.replace(old_init, new_init, 1)

    old_q = (
        '      startQ = uq < 0 ? 0 : uq;\n'
        '    }\n'
        '    showQuestion(startQ);\n'
    )
    new_q = (
        '      startQ = uq < 0 ? 0 : uq;\n'
        '    }\n'
        '    if (!wantResults) showQuestion(startQ);\n'
    )
    if old_q in text and 'if (!wantResults) showQuestion(startQ);' not in text:
        text = text.replace(old_q, new_q, 1)

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
