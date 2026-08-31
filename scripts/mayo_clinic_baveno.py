#!/usr/bin/env python3
from pathlib import Path
import runpy

for name in ("index.html", "hcc-simulator.html"):
    src = Path(name)
    if not src.exists():
        print("skip", name)
        continue
    Path("/tmp/gh-index.html").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    s = Path("/tmp/gh-index.html").read_text(encoding="utf-8")
    if 'step-label">1 of 8' in s and "htmlOut = recLead +" in s and "PMID 42624290" in s:
        print("already patched", name)
        continue
    runpy.run_path("scripts/patch_mayo_engine.py")
    src.write_text(Path("/tmp/gh-index.html").read_text(encoding="utf-8"), encoding="utf-8")
    print("patched", name)
