#!/usr/bin/env python3
"""Assemble Mayo MDT live HTML: Q1 MVI 1of8, Zuo/Su Y GAP cards, cream/navy lock, iPad polish."""
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
#resPresetBar { display: none !important; }
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

def upsert_zuo(html):
    marker = "Zuo M HAIC+camrelizumab+apatinib TRIPLET"
    if marker in html:
        h = html.find(marker)
        h4 = html.rfind("<h4", 0, h)
        ul = html.find("</ul>", h)
        if h4 >= 0 and ul > h4:
            html = html[:h4] + ZUO_CARD.strip() + html[ul + 5:]
            html = re.sub(r"(</ul>)\n{3,}<h4", r"\1\n\n      <h4", html, count=3)
            return html
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
            return html[: ul + 5] + "\n" + ZUO_CARD + html[ul + 5 :]
        h = html.rfind("<h4", 0, i)
        if h < 0:
            h = html.rfind("<h3", 0, i)
        if h < 0:
            h = i
        return html[:h] + "\n" + ZUO_CARD + "\n" + html[h:]
    raise SystemExit("no insert anchor for Zuo M card")

s = upsert_zuo(s)

if decide_i >= 0:
    new_i = s.find("function decide()")
    if s[new_i: new_i + 5000] != decide_slice:
        raise SystemExit("decide() drifted")

if "1 of 8" not in s or "function decide()" not in s:
    raise SystemExit("payload incomplete")
if "38961006" not in s or s.count("Zuo M HAIC+camrelizumab+apatinib TRIPLET") != 1:
    raise SystemExit("Zuo card missing or duplicated")

(root / "index.html").write_text(s, encoding="utf-8")
(root / "hcc-simulator.html").write_text(s, encoding="utf-8")
print("assembled", len(s), "zuo", "38961006" in s, "recLead", "const htmlOut = recLead +" in s, "gates", "8 gates" in s)
