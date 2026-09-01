#!/usr/bin/env python3
"""Assemble Mayo MDT live HTML. Prefer gzip payload; else polish + upsert cards. Do not restack."""
from pathlib import Path
import gzip, base64, hashlib, re

root = Path(__file__).resolve().parents[1]
pay = Path(__file__).resolve().parent / "payload"


def decode_payload() -> str | None:
    parts = sorted(pay.glob("live_mdt_*.b64"))
    if len(parts) < 3:
        return None
    chunks = []
    for part in parts:
        chunks.append("".join(part.read_text(encoding="ascii").split()))
    html = gzip.decompress(base64.b64decode("".join(chunks))).decode("utf-8")
    need = (
        "1 of 8 — Macrovascular invasion",
        "function decide()",
        "TIE_BAND = 5",
        "LEAN_BAND = 8",
        "const htmlOut = recLead +",
        "Chi CT / Huang YH Taipei-VGH IO selection review",
        "2026 KLCA-NCC Korea CPG — MODELLED/GAP",
        "Lee IC TLCA intermediate-stage consensus",
    )
    for n in need:
        if n not in html:
            raise SystemExit(f"payload missing {n}")
    if "1 of 10" in html:
        raise SystemExit("payload still has 1 of 10")
    return html
