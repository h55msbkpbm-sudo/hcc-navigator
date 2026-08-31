#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, urllib.request
root = Path(__file__).resolve().parents[1]
payload = root / "scripts" / "payload"
html = None
su = list(payload.glob("su_gz*.b64")) if payload.exists() else []
if su:
    blob = "".join((payload / f"su_gz{i}.b64").read_text() for i in range(8))
    html = gzip.decompress(base64.b64decode(blob)).decode("utf-8")
elif payload.exists() and list(payload.glob("gz*.b64")):
    blob = "".join((payload / f"gz{i}.b64").read_text() for i in range(3))
    html = gzip.decompress(base64.b64decode(blob)).decode("utf-8")
else:
    raise SystemExit("no payload")
if "1 of 8" not in html or "function decide()" not in html:
    raise SystemExit("payload incomplete")
(root / "index.html").write_text(html, encoding="utf-8")
(root / "hcc-simulator.html").write_text(html, encoding="utf-8")
print("assembled", len(html), "Su Y" in html, "1802197" in html)
