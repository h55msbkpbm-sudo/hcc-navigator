#!/usr/bin/env python3
"""Assemble Mayo MDT payload onto index.html + hcc-simulator.html."""
from pathlib import Path
import base64, gzip, sys

ROOT = Path('.')
PAY = ROOT / 'scripts' / 'payload'
parts = sorted(PAY.glob('c*.b64'), key=lambda p: int(p.stem[1:]))
if not parts:
    sys.exit('no payload chunks')
b64 = ''.join(p.read_text().strip() for p in parts)
html = gzip.decompress(base64.b64decode(b64)).decode('utf-8')
assert '1 of 8' in html
assert 'Macrovascular invasion' in html
assert 'function decide()' in html
assert 'PMID 42664455' in html
assert 'const htmlOut = recLead +' in html
assert '#e4c56a' not in html
for p in (ROOT / 'index.html', ROOT / 'hcc-simulator.html'):
    p.write_text(html, encoding='utf-8')
    print('wrote', p, len(html))
