#!/usr/bin/env python3
"""Assemble Mayo MDT live HTML from repo index.html + Q1 MVI cards + cream/navy lock."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "index.html"
cards_path = root / "scripts" / "payload" / "q1_mvi_cards.html"

if not src.exists():
    raise SystemExit("index.html missing")

s = src.read_text(encoding="utf-8")
decide_i = s.find("function decide()")
decide_slice = s[decide_i: decide_i + 5000] if decide_i >= 0 else ""

repls = (
    ("#e4c56a", "#003da5"),
    ("#E4C56A", "#003da5"),
    ("#0f766e", "#003da5"),
    ("#0F766E", "#003da5"),
    ("#2dd4bf", "#93c5fd"),
    ("#2DD4BF", "#93c5fd"),
    ("#5eead4", "#93c5fd"),
    ("#5EEAD4", "#93c5fd"),
    ("#14b8a6", "#003da5"),
    ("rgba(20, 184, 166,", "rgba(0, 61, 165,"),
    ("rgba(15, 118, 110,", "rgba(0, 61, 165,"),
    ("rgba(176, 137, 46,", "rgba(0, 61, 165,"),
    ("rgba(176,137,46,", "rgba(0, 61, 165,"),
    ("background-color: #ffffff;", "background-color: #f4f1ea;"),
    ("html, body, .app, .main { background: #ffffff !important; }",
     "html, body, .app, .main { background: #f4f1ea !important; }"),
    ("/* no atlas grid — Mayo pages are plain white */",
     "/* no atlas grid — Mayo cream page */"),
    ("1 of 10 — Number of intrahepatic lesions",
     "1 of 8 — Macrovascular invasion (Vp0–Vp4 / HV-IVC)"),
    ("1 of 10", "1 of 8"),
    ("<h1>Number of intrahepatic lesions</h1>",
     "<h1>Macrovascular invasion (Vp0–Vp4 / HV-IVC)</h1>"),
    ("Answered <b>0</b> / 6", "Answered <b>0</b> / 8"),
)
for a, b in repls:
    s = s.replace(a, b)

if "const htmlOut = matchLead +" in s and "const htmlOut = recLead +" not in s:
    s = s.replace("const htmlOut = matchLead +", "const htmlOut = recLead +", 1)

if "leftover Mayo lock" not in s:
    lock = (
        "\n/* leftover Mayo lock — cream page, navy header, Continue #002f7a */\n"
        "html, body, .app, .main { background: #f4f1ea !important; }\n"
        "body { background-color: #f4f1ea !important; }\n"
        ".topbar, .mayo-lockup, header.topbar { background: #003da5 !important; color: #fffcf7 !important; }\n"
        ".btn-primary, #next0, #next1, #next2, button.btn-primary { background: #002f7a !important; color: #fffcf7 !important; }\n"
    )
    last = s.rfind("</style>")
    if last > 0:
        s = s[:last] + lock + s[last:]

if "Su Y TACE+LEN+envafolimab conversion pilot" not in s:
    cards = ""
    if cards_path.exists():
        cards = cards_path.read_text(encoding="utf-8").strip()
    if "Su Y TACE+LEN+envafolimab conversion pilot" not in cards:
        cards = """
      <h4 style=\"font-size:13px;margin:0 0 8px;color:var(--gray-700)\">Su Y TACE+LEN+envafolimab conversion pilot — MODELLED/GAP (Q1 MVI)</h4>
      <ul style=\"margin:0 0 14px 18px;font-size:12.5px;line-height:1.55;color:var(--gray-700)\">
        <li><a href=\"https://doi.org/10.3389/fimmu.2026.1802197\" target=\"_blank\" rel=\"noopener\">Su Y, Liang Y, Zhong D et al. TACE plus lenvatinib and envafolimab for conversion therapy in unresectable HCC</a> — <em>Front Immunol</em>. 2026;17:1802197. DOI 10.3389/fimmu.2026.1802197. ChiCTR2400081945. Sichuan Cancer Hospital pilot. n=15, BCLC B/C. Printed only: mRECIST ORR 53.3%; DCR 86.7%; conversion 9/15 (60%), all R0; pCR/MPR 5/9 (55.6%); mPFS 12.0 mo; 1-year OS 100%; 18-month OS 93.3%; grade ≥3 TRAE 53.3%; GI bleed 6/15 (40%), including 1 grade 3. Distinct from Chen STTT 2024 envafolimab+LEN+TACE phase 2 (NCT05213221). Mapped to Q1 Macrovascular (Vp0–Vp4). <strong>MODELLED/GAP:</strong> Asia-enriched TACE+LEN+envafolimab conversion pilot — not a 1L rank vs IMbrave150 / HIMALAYA / CheckMate 9DW. Dual-eligibility A+B vs STRIDE unchanged. ORIENT-32 / CARES-310 stay Asia-enriched. HKLC / CUSE stay in closed Details.</li>
      </ul>
"""
    inserted = False
    for anc in (
        "DHDC vs DDC donafenib+camrelizumab — MODELLED/GAP</h4>",
        "DHDC vs DDC",
        "Guidelines & strategy",
    ):
        i = s.find(anc)
        if i < 0:
            continue
        h = s.rfind("<h4", 0, i)
        if h < 0:
            h = s.rfind("<h3", 0, i)
        if h < 0:
            h = i
        s = s[:h] + "\n" + cards + "\n" + s[h:]
        inserted = True
        break
    if not inserted:
        raise SystemExit("no insert anchor for Q1 MVI cards")

if "Zuo M HAIC+camrelizumab+apatinib TRIPLET" not in s:
    zuo = """
      <h4 style=\"font-size:13px;margin:0 0 8px;color:var(--gray-700)\">Zuo M HAIC+camrelizumab+apatinib TRIPLET — MODELLED/GAP (Q1 MVI)</h4>
      <ul style=\"margin:0 0 14px 18px;font-size:12.5px;line-height:1.55;color:var(--gray-700)\">
        <li><a href=\"https://doi.org/10.1007/s12072-024-10690-6\" target=\"_blank\" rel=\"noopener\">Zuo M, Cao Y, Yang Y et al. Hepatic arterial infusion chemotherapy plus camrelizumab and apatinib for advanced hepatocellular carcinoma</a> — <em>Hepatol Int</em>. 2024;18:1486–1498. DOI 10.1007/s12072-024-10690-6. PMID 38961006. PMCID PMC11461759. ChiCTR2300075828. SYSUCC retrospective RWE. n=416 (TRIPLET HAIC+camrelizumab+apatinib 207 vs C-A camrelizumab+apatinib 209); after 1:1 PSM 109/arm. Printed only: mOS NR vs 19.9 mo (p<0.001); mPFS 11.5 vs 9.6 mo (p<0.001); grade 3/4 AE 82.1% vs 71.3%. Distinct from Zhang STTT 2023 NCT04191889 TRIPLET phase 2 single-arm and from Zuo WJGO 2024 TRIPLET±MWA. Mapped to Q1 Macrovascular (Vp0–Vp4). <strong>MODELLED/GAP:</strong> Asia-enriched HAIC-add-on RWE on a camrelizumab+apatinib backbone — not a 1L rank vs IMbrave150 / HIMALAYA / CheckMate 9DW and does not displace A+B vs STRIDE. Dual-eligibility A+B vs STRIDE unchanged. CARES-310 stays the cited camre+rivoceranib 1L RCT. ORIENT-32 / CARES-310 stay Asia-enriched. HKLC / CUSE stay in closed Details.</li>
      </ul>
"""
    inserted = False
    for anc in (
        "Su Y TACE+LEN+envafolimab conversion pilot — MODELLED/GAP (Q1 MVI)</h4>",
        "DHDC vs DDC donafenib+camrelizumab — MODELLED/GAP</h4>",
        "DHDC vs DDC",
        "Guidelines & strategy",
    ):
        i = s.find(anc)
        if i < 0:
            continue
        if anc.startswith("Su Y"):
            ul = s.find("</ul>", i)
            if ul < 0:
                continue
            s = s[: ul + 5] + "\n" + zuo + s[ul + 5 :]
        else:
            h = s.rfind("<h4", 0, i)
            if h < 0:
                h = s.rfind("<h3", 0, i)
            if h < 0:
                h = i
            s = s[:h] + "\n" + zuo + "\n" + s[h:]
        inserted = True
        break
    if not inserted:
        raise SystemExit("no insert anchor for Zuo M card")

if decide_i >= 0:
    new_i = s.find("function decide()")
    if s[new_i: new_i + 5000] != decide_slice:
        raise SystemExit("decide() drifted")

if "1 of 8" not in s or "function decide()" not in s:
    raise SystemExit("payload incomplete")

(root / "index.html").write_text(s, encoding="utf-8")
(root / "hcc-simulator.html").write_text(s, encoding="utf-8")
print(
    "assembled",
    len(s),
    "su",
    "Su Y TACE+LEN+envafolimab" in s,
    "1802197" in s,
    "nct",
    "NCT05213221" in s,
    "zuo",
    "38961006" in s,
    "recLead",
    "const htmlOut = recLead +" in s,
)
