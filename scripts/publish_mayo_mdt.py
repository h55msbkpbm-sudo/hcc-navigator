#!/usr/bin/env python3
from pathlib import Path
import base64, gzip
root = Path(__file__).resolve().parents[1]
payload = root / "scripts" / "payload"
gz_parts = list(payload.glob("gz*.b64"))
txt_parts = list(payload.glob("part*.txt"))
if gz_parts:
    blob = "".join((payload / f"gz{i}.b64").read_text() for i in range(3))
    html = gzip.decompress(base64.b64decode(blob)).decode("utf-8")
elif txt_parts:
    html = "".join(p.read_text(encoding="utf-8") for p in sorted(txt_parts))
else:
    raise SystemExit("no payload")
if "Pham AG" not in html or "1 of 8" not in html:
    raise SystemExit("payload incomplete")
(root / "index.html").write_text(html, encoding="utf-8")
(root / "hcc-simulator.html").write_text(html, encoding="utf-8")
print("assembled", len(html))
