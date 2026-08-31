#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
parts = sorted((root / "scripts" / "payload").glob("part*.txt"))
html = "".join(p.read_text(encoding="utf-8") for p in parts)
if "Pham AG" not in html or "1 of 8" not in html:
    raise SystemExit("payload incomplete")
(root / "index.html").write_text(html, encoding="utf-8")
(root / "hcc-simulator.html").write_text(html, encoding="utf-8")
print("assembled", len(html), "parts", len(parts))
