#!/usr/bin/env python3
"""Assemble Mayo MDT live HTML. Mutate existing index; upsert GAP cards. Do not restack."""
from pathlib import Path
import hashlib, re

root = Path(__file__).resolve().parents[1]
pay = Path(__file__).resolve().parent / "payload"

LIVE_CSS = """
/* MDT live lock — cream page, navy chrome, Continue #002f7a */
html, body, .app, .main, .trust-bar, .mobile-steps { background: #f4f1ea !important; }
body { background-color: #f4f1ea !important; }
.topbar, .mayo-lockup, header.topbar { background: #003da5 !important; color: #fffcf7 !important; }
.btn-primary, #next0, #next1, #next2, button.btn-primary {
  background: #002f7a !important; color: #fffcf7 !important; box-shadow: none !important; border: 0 !important;
}
.step-label {
  color: #003da5 !important; background: #eef2f8 !important;
  border: 1px solid rgba(0, 47, 122, .18) !important; border-left: 3px solid #003da5 !important;
}
.step-meta, .miss-list, #resPresetBar, #presetBar, .preset-bar { display: none !important; }
.card.adv-only, #burdenCalcCard, .atlas { display: none !important; }
.res-banner { border-radius: 2px !important; box-shadow: none !important; }
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
  .step h1 { font-size: 28px !important; }
  .btn, .btn-primary, #next0, #next1, #next2 { min-height: 48px !important; }
}
"""

MARKERS = (
    "Chi CT / Huang YH Taipei-VGH IO selection review",
    "2026 KLCA-NCC Korea CPG — MODELLED/GAP",
    "Lee IC TLCA intermediate-stage consensus",
    "Wu S Vp4 HAICAC",
    "Yang DL / Ye L GUIDANCE001 TACE",
    "Zhang X LEN-TAP phase 2 conversion",
)


def upsert_block(html, marker, block, anchors):
    if marker in html:
        h = html.find(marker)
        h4 = html.rfind("<h4", 0, h)
        ul = html.find("</ul>", h)
        if h4 >= 0 and ul > h4:
            return html[:h4] + block.strip() + html[ul + 5 :]
        return html
    for anc in anchors:
        i = html.find(anc)
        if i < 0:
            continue
        ul = html.find("</ul>", i)
        if ul < 0:
            continue
        return html[: ul + 5] + "\n" + block + html[ul + 5 :]
    for anc in ("Guidelines & strategy", "DHDC vs DDC"):
        i = html.find(anc)
        if i >= 0:
            h = html.rfind("<h4", 0, i)
            if h < 0:
                h = i
            return html[:h] + "\n" + block + "\n" + html[h:]
    raise SystemExit("no insert anchor for " + marker)


def split_cards(raw):
    parts = re.split(r"(?=<h4 )", raw)
    out = []
    for p in parts:
        p = p.strip()
        if not p.startswith("<h4"):
            continue
        for marker in MARKERS:
            if marker in p:
                out.append((marker, p))
                break
    return out


def mutate(s):
    decide_i = s.find("function decide()")
    decide_slice = s[decide_i : decide_i + 5000] if decide_i >= 0 else ""
    pairs = (
        ("1 of 10 — Number of intrahepatic lesions", "1 of 8 — Macrovascular invasion (Vp0–Vp4 / HV-IVC)"),
        ("1 of 10", "1 of 8"),
        ("<h1>Number of intrahepatic lesions</h1>", "<h1>Macrovascular invasion (Vp0–Vp4 / HV-IVC)</h1>"),
        ("<h1>Number of lesions</h1>", "<h1>Macrovascular invasion (Vp0–Vp4 / HV-IVC)</h1>"),
        ("<h1>Macrovascular invasion</h1>", "<h1>Macrovascular invasion (Vp0–Vp4 / HV-IVC)</h1>"),
        ('<div class="step-label">1 of 8</div>', '<div class="step-label">1 of 8 — Macrovascular invasion (Vp0–Vp4 / HV-IVC)</div>'),
        ('<div class="lbl">Comparison</div>', '<div class="lbl">Recommendation</div>'),
        ("recKey === 'incomplete' ? 'Results' : 'Comparison'", "recKey === 'incomplete' ? 'Results' : 'Recommendation'"),
        (
            "  if (h1) h1.textContent = (qIndex + 1) + '. ' + q.h;\n  if (lead) lead.textContent = q.lead || '';\n  if (lab) lab.textContent = (qIndex + 1) + ' of ' + QFLOW.length;",
            "  if (h1) h1.textContent = q.h;\n  if (lead) lead.textContent = q.lead || '';\n  if (lab) lab.textContent = (qIndex + 1) + ' of ' + QFLOW.length + ' — ' + q.h;",
        ),
        ("See recommendation →", "Recommendation →"),
        ("Answered <b>0</b> / 6", "Answered <b>0</b> / 8"),
        ("Answered <b>0</b> / 4", "Answered <b>0</b> / 8"),
        ("#e4c56a", "#003da5"),
        ("#0f766e", "#003da5"),
        ("#14b8a6", "#003da5"),
        ("background-color: #ffffff;", "background-color: #f4f1ea;"),
        (
            "<strong>iPad / iPhone:</strong> If buttons do not respond, open this page in Safari. In-app OneDrive or Files preview blocks JavaScript.",
            "<strong>iPad:</strong> Open in Safari if taps do not register.",
        ),
        ("Finish remaining first-pass items.", "Finish the remaining gates."),
        ("NCCN 2026 · BCLC 2026 · 8 gates, starting at macrovascular invasion", "NCCN 2026 · BCLC 2026 · 8 gates · Q1 macrovascular"),
        ("Lesion count · Largest size · Macrovascular invasion · Extrahepatic spread", "Macrovascular invasion · Extrahepatic spread"),
    )
    for a, b in pairs:
        s = s.replace(a, b)
    if "const htmlOut = matchLead +" in s and "const htmlOut = recLead +" not in s:
        s = s.replace("const htmlOut = matchLead +", "const htmlOut = recLead +", 1)
    if "MDT live lock — cream page" not in s:
        last = s.rfind("</style>")
        if last > 0:
            s = s[:last] + LIVE_CSS + s[last:]
    cards_path = pay / "gap_cards.html"
    if cards_path.exists():
        raw = cards_path.read_text(encoding="utf-8")
        anchors = (
            "Wu C VP4 HAIC+LEN+PD-1 — MODELLED/GAP (Q1 MVI)</h4>",
            "Yalikun K HAIC+camrelizumab+apatinib conversion — MODELLED/GAP (Q1 MVI)</h4>",
            "Zuo M HAIC+camrelizumab+apatinib TRIPLET — MODELLED/GAP (Q1 MVI)</h4>",
            "Su Y TACE+LEN+envafolimab conversion pilot — MODELLED/GAP (Q1 MVI)</h4>",
            "DHDC vs DDC donafenib+camrelizumab — MODELLED/GAP</h4>",
            "Guidelines & strategy",
        )
        for marker, block in split_cards(raw):
            s = upsert_block(s, marker, block, anchors)
    if decide_i >= 0:
        new_i = s.find("function decide()")
        if new_i < 0 or s[new_i : new_i + 5000] != decide_slice:
            raise SystemExit("decide() drifted")
    if "1 of 10" in s:
        raise SystemExit("1 of 10 leftover")
    if "Chi CT / Huang YH Taipei-VGH IO selection review" not in s:
        raise SystemExit("Chi card missing")
    if "TIE_BAND" not in s:
        raise SystemExit("TIE_BAND lost")
    return s


def main():
    src = root / "index.html"
    if not src.exists():
        raise SystemExit("index.html missing")
    html = mutate(src.read_text(encoding="utf-8"))
    (root / "index.html").write_text(html, encoding="utf-8")
    (root / "hcc-simulator.html").write_text(html, encoding="utf-8")
    print("wrote mutate", len(html), "md5", hashlib.md5(html.encode()).hexdigest())
    print("q1", "1 of 8 — Macrovascular" in html, "chi", "42007976" in html, "tlca", "40755008" in html, "klca", "cmh.2026.0943" in html, "decide", "function decide()" in html)


if __name__ == "__main__":
    main()
