#!/usr/bin/env python3
"""v2: delete dead _portraitRemoved and hide .pt-pic."""
from pathlib import Path
import re

FN_STUB = "function patientPictureHtml() { return ''; }\n"
HIDE_CSS = ".pt-pic, figure.pt-pic { display: none !important; }\n"

def patch(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    orig = text
    text = re.sub(
        r"function patientPictureHtml\(\) \{ return ''; \}\nfunction _portraitRemoved\(\) \{[\s\S]*?\n\}\n",
        FN_STUB,
        text,
        count=1,
    )
    text = re.sub(
        r"function _portraitRemoved\(\) \{[\s\S]*?\n\}\n",
        "",
        text,
        count=1,
    )
    text = re.sub(
        r"\.pt-pic \{[\s\S]*?\.pt-pic figcaption span \{[^}]+\}\n",
        HIDE_CSS,
        text,
        count=1,
    )
    text = text.replace("\n    patientPictureHtml();", "")
    if text != orig:
        path.write_text(text, encoding='utf-8')
        print(path.name, 'wrote', path.stat().st_size)
    else:
        print(path.name, 'already clean')

if __name__ == '__main__':
    for name in ('index.html', 'hcc-simulator.html'):
        p = Path(name)
        if p.exists():
            patch(p)
