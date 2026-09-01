#!/usr/bin/env python3
"""Assemble Mayo MDT live HTML: Q1 MVI 1of8, Yalikun/Zuo/Su Y GAP cards, cream/navy lock, iPad polish."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
src = root / "index.html"
cards_path = root / "scripts" / "payload" / "q1_mvi_cards.html"

if not src.exists():
    raise SystemExit("index.html missing")

s = src.read_text(encoding="utf-8")
decide_i = s.find("function decide()")
decide_slice = s[decide_i: decide_i + 5000] if decide_i >= 0 else ""

LIVE_CSS = """
/* Live MDT / iPad presentation polish */
.step-meta, .miss-list { display: none !important; }
.res-banner { border-radius: 2px !important; box-shadow: none !important; }
#resPresetBar, #presetBar, .preset-bar { display: none !important; }
.step-label { color: #003da5 !important; background: #eef2f8 !important; border-left-color: #003da5 !important; }
@media (max-width: 1180px) {
  .app { grid-template-columns: minmax(0, 1fr) !important; }
  .sidebar, .panel { display: none !important; }
  .main { max-width: 720px; margin: 0 auto; padding: 20px 24px 48px; }
}
@media (orientation: landscape) and (min-width: 768px) and (max-width: 1366px) {
  .app { grid-template-columns: minmax(0, 1fr) !important; }
  .sidebar, .panel { display: none !important; }
  .main { max-width: 760px; margin: 0 auto; }
  .opt { min-height: 64px !important; padding: 14px 16px !important; }
  .step h1 { font-size: 28px !important; letter-spacing: -.3px; }
  .btn, .btn-primary, #next0, #next1, #next2 { min-height: 48px !important; }
  .res-banner { padding: 20px 22px !important; }
  .res-banner h2 { font-size: 26px !important; }
}
"""

ZUO_CARD = """
      <h4 style=\"font-size:13px;margin:0 0 8px;color:var(--gray-700)\">Zuo M HAIC+camrelizumab+apatinib TRIPLET — MODELLED/GAP (Q1 MVI)</h4>
      <ul style=\"margin:0 0 14px 18px;font-size:12.5px;line-height:1.55;color:var(--gray-700)\">
        <li><a href=\"https://doi.org/10.1007/s12072-024-10690-6\" target=\"_blank\" rel=\"noopener\">Zuo M, Cao Y, Yang Y et al. Hepatic arterial infusion chemotherapy plus camrelizumab and apatinib for advanced hepatocellular carcinoma</a> — <em>Hepatol Int</em>. 2024;18:1486–1498. DOI 10.1007/s12072-024-10690-6. PMID 38961006. PMCID PMC11461759. ChiCTR2300075828. SYSUCC retrospective RWE. n=416 (TRIPLET HAIC+camrelizumab+apatinib 207 vs C-A camrelizumab+apatinib 209); after 1:1 PSM 109/arm. Printed only: mOS NR vs 19.9 mo; mPFS 11.5 vs 9.6 mo; G3/4 AE 82.1% vs 71.3%. Distinct from Zhang STTT 2023 NCT04191889 TRIPLET phase 2 single-arm and from Zuo WJGO 2024 TRIPLET±MWA. Mapped to Q1 Macrovascular (Vp0–Vp4). <strong>MODELLED/GAP:</strong> Asia-enriched HAIC-add-on RWE on a camrelizumab+apatinib backbone — not a 1L rank vs IMbrave150 / HIMALAYA / CheckMate 9DW and does not displace A+B vs STRIDE. Dual-eligibility A+B vs STRIDE unchanged when scores are close (TIE 5 / LEAN 8). CARES-310 stays the cited camre+rivoceranib 1L RCT. ORIENT-32 / CARES-310 stay Asia-enriched. HKLC / CUSE stay in closed Details.</li>
      </ul>
"""

YALIKUN_CARD = """
      <h4 style=\"font-size:13px;margin:0 0 8px;color:var(--gray-700)\">Yalikun K HAIC+camrelizumab+apatinib conversion — MODELLED/GAP (Q1 MVI)</h4>
      <ul style=\"margin:0 0 14px 18px;font-size:12.5px;line-height:1.55;color:var(--gray-700)\">
        <li><a href=\"https://doi.org/10.1186/s12885-025-14250-5\" target=\"_blank\" rel=\"noopener\">Yalikun K, Li Z, Zhang J et al. Hepatic artery infusion chemotherapy combined with camrelizumab and apatinib as conversion therapy for patients with unresectable hepatocellular carcinoma: a single-arm exploratory trial</a> — <em>BMC Cancer</em>. 2025;25:838. DOI 10.1186/s12885-025-14250-5. PMID 40335980. PMCID PMC12056981. NCT05099848. Shandong Cancer Hospital single-arm exploratory conversion pilot. n=19. Printed only: conversion 14/19 (73.7%); R0 9/19 (47.4%); MPR 3/9; pCR 2/9; RECIST ORR 47.4% DCR 89.5%; mRECIST ORR/DCR 89.5%; 1-year OS 73.7%; 2-year OS 63.2%. Distinct from Zuo M Hepatol Int PMID 38961006 (HAIC+camre+apa PSM RWE, not conversion pilot), Zhang STTT 2023 NCT04191889 TRIPLET phase 2, Zhang W Front Immunol PMID 40529364, LEN-TAP PMID 41565617, PLATIC PMID 42092358, GUIDANCE007, HILL, CHANCE 2416, and Weng PMID 42666210. Mapped to Q1 Macrovascular (Vp0–Vp4). <strong>MODELLED/GAP:</strong> Asia-enriched HAIC+camrelizumab+apatinib conversion pilot — not a 1L rank vs IMbrave150 / HIMALAYA / CheckMate 9DW and does not displace A+B vs STRIDE. Dual-eligibility A+B vs STRIDE unchanged when scores are close (TIE 5 / LEAN 8). CARES-310 stays the cited camre+rivoceranib 1L RCT. ORIENT-32 / CARES-310 stay Asia-enriched. HKLC / CUSE stay in closed Details.</li>
      </ul>
"""

SU_CARD = """
      <h4 style=\"font-size:13px;margin:0 0 8px;color:var(--gray-700)\">Su Y TACE+LEN+envafolimab conversion pilot — MODELLED/GAP (Q1 MVI)</h4>
      <ul style=\"margin:0 0 14px 18px;font-size:12.5px;line-height:1.55;color:var(--gray-700)\">
        <li><a href=\"https://doi.org/10.3389/fimmu.2026.1802197\" target=\"_blank\" rel=\"noopener\">Su Y, Liang Y, Zhong D et al. TACE plus lenvatinib and envafolimab for conversion therapy in unresectable HCC</a> — <em>Front Immunol</em>. 2026;17:1802197. DOI 10.3389/fimmu.2026.1802197. ChiCTR2400081945. Sichuan Cancer Hospital pilot. n=15, BCLC B/C. Printed only: mRECIST ORR 53.3%; DCR 86.7%; conversion 9/15 (60%), all R0; pCR/MPR 5/9 (55.6%); mPFS 12.0 mo; 1-year OS 100%; 18-month OS 93.3%; grade ≥3 TRAE 53.3%; GI bleed 6/15 (40%), including 1 grade 3. Distinct from Chen STTT 2024 envafolimab+LEN+TACE phase 2 (NCT05213221). Mapped to Q1 Macrovascular (Vp0–Vp4). <strong>MODELLED/GAP:</strong> Asia-enriched TACE+LEN+envafolimab conversion pilot — not a 1L rank vs IMbrave150 / HIMALAYA / CheckMate 9DW. Dual-eligibility A+B vs STRIDE unchanged. ORIENT-32 / CARES-310 stay Asia-enriched. HKLC / CUSE stay in closed Details.</li>
      </ul>
"""

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
    ("rgba(13,115,119,", "rgba(0, 61, 165,"),
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
    ("Answered <b>0</b> / 4", "Answered <b>0</b> / 8"),
    ("Based on NCCN 2026 and BCLC 2026 · 8 gating questions, starting at macrovascular invasion",
     "NCCN 2026 · BCLC 2026 · 8 gates, starting at macrovascular invasion"),
    ("<strong>iPad / iPhone:</strong> If buttons do not respond, open this page in Safari. In-app OneDrive or Files preview blocks JavaScript.",
     "<strong>iPad:</strong> Open in Safari if taps do not register."),
    ("Finish remaining first-pass items.", "Finish the remaining gates."),
    ("lead:'Required before atezolizumab + bevacizumab (HA HAB-P365).'",
     "lead:'Required before A+B (HAB-P365).'"),
    ("lead:'Select all that apply. Active autoimmune blocks the IO pathway.'",
     "lead:'Select all that apply. Active autoimmune blocks IO.'"),
    ('<div class="lbl">Comparison</div>', '<div class="lbl">Recommendation</div>'),
    ("recKey === 'incomplete' ? 'Results' : 'Comparison'",
     "recKey === 'incomplete' ? 'Results' : 'Recommendation'"),
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

if "Live MDT / iPad presentation polish" not in s:
    last = s.rfind("</style>")
    if last > 0:
        s = s[:last] + LIVE_CSS + s[last:]

if "Su Y TACE+LEN+envafolimab conversion pilot" not in s:
    cards = ""
    if cards_path.exists():
        cards = cards_path.read_text(encoding="utf-8").strip()
    if "Su Y TACE+LEN+envafolimab conversion pilot" not in cards:
        cards = SU_CARD
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


def upsert_zuo(html: str) -> str:
    marker = "Zuo M HAIC+camrelizumab+apatinib TRIPLET"
    if marker in html:
        return html
    inserted = False
    for anc in (
        "Su Y TACE+LEN+envafolimab conversion pilot — MODELLED/GAP (Q1 MVI)</h4>",
        "DHDC vs DDC donafenib+camrelizumab — MODELLED/GAP</h4>",
        "DHDC vs DDC",
        "Guidelines & strategy",
    ):
        i = html.find(anc)
        if i < 0:
            continue
        if anc.startswith("Su Y"):
            ul = html.find("</ul>", i)
            if ul < 0:
                continue
            html = html[: ul + 5] + "\n" + ZUO_CARD + html[ul + 5 :]
        else:
            h = html.rfind("<h4", 0, i)
            if h < 0:
                h = html.rfind("<h3", 0, i)
            if h < 0:
                h = i
            html = html[:h] + "\n" + ZUO_CARD + "\n" + html[h:]
        inserted = True
        break
    if not inserted:
        raise SystemExit("no insert anchor for Zuo M card")
    return html


s = upsert_zuo(s)


def upsert_yalikun(html: str) -> str:
    marker = "Yalikun K HAIC+camrelizumab+apatinib conversion"
    if marker in html:
        return html
    for anc in (
        "Zhang W HAIC+LEN+PD-1/L1 conversion — MODELLED/GAP (Q1 MVI)</h4>",
        "Zuo M HAIC+camrelizumab+apatinib TRIPLET — MODELLED/GAP (Q1 MVI)</h4>",
        "DHDC vs DDC donafenib+camrelizumab — MODELLED/GAP</h4>",
        "DHDC vs DDC",
        "Guidelines & strategy",
    ):
        i = html.find(anc)
        if i < 0:
            continue
        ul = html.find("</ul>", i)
        if ul < 0:
            continue
        html = html[: ul + 5] + "\n" + YALIKUN_CARD + html[ul + 5 :]
        html = re.sub(r"(</ul>)\n{3,}<h4", r"\1\n\n      <h4", html, count=3)
        return html
    raise SystemExit("no insert anchor for Yalikun card")


s = upsert_yalikun(s)

if decide_i >= 0:
    new_i = s.find("function decide()")
    if s[new_i: new_i + 5000] != decide_slice:
        raise SystemExit("decide() drifted")

if "1 of 8" not in s or "function decide()" not in s:
    raise SystemExit("payload incomplete")
if "38961006" not in s or "ChiCTR2300075828" not in s:
    raise SystemExit("Zuo card missing after assemble")
if s.count("Zuo M HAIC+camrelizumab+apatinib TRIPLET") != 1:
    raise SystemExit("Zuo card count drifted")
if "40335980" not in s or "NCT05099848" not in s:
    raise SystemExit("Yalikun card missing after assemble")
if s.count("Yalikun K HAIC+camrelizumab+apatinib conversion") != 1:
    raise SystemExit("Yalikun card count drifted")

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
    "yalikun",
    "40335980" in s,
    "recLead",
    "const htmlOut = recLead +" in s,
    "gates",
    "8 gates" in s,
    "lblRec",
    '<div class="lbl">Recommendation</div>' in s,
    "ipadCss",
    "Live MDT / iPad presentation polish" in s,
)
