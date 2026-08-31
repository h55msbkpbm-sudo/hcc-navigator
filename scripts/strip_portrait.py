#!/usr/bin/env python3
"""Strip Results patient portrait from index.html and hcc-simulator.html."""
from pathlib import Path

JOIN_OLD = "    patientPictureHtml();"
FN_OLD = "function patientPictureHtml() {"
FN_STUB = "function patientPictureHtml() { return ''; }\nfunction _portraitRemoved() {"
WIPE = "  document.querySelectorAll('.burden-map, figure.pt-pic, .pt-pic, #burdenCalcCard').forEach(function(el){ el.remove(); });\n"
INNER = "  if (_rb) _rb.innerHTML = htmlOut;\n"


def patch(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    changed = False
    if "function patientPictureHtml() { return ''; }" not in text and FN_OLD in text:
        text = text.replace(FN_OLD, FN_STUB, 1)
        changed = True
        print(path.name, "stubbed patientPictureHtml")
    if JOIN_OLD in text:
        text = text.replace(
            "    `<details class=\"mdt-fold\" id=\"res-details\"><summary>Details</summary><div class=\"fold-body\">${designLead}<details class=\"mdt-fold\" id=\"fold-efficacy\"><summary>Phase 3 efficacy</summary><div class=\"fold-body\">${efficacyLead}</div></details>${rec5yHtml}${detailInner}</div></details>` +\n    patientPictureHtml();",
            "    `<details class=\"mdt-fold\" id=\"res-details\"><summary>Details</summary><div class=\"fold-body\">${designLead}<details class=\"mdt-fold\" id=\"fold-efficacy\"><summary>Phase 3 efficacy</summary><div class=\"fold-body\">${efficacyLead}</div></details>${rec5yHtml}${detailInner}</div></details>`;",
            1,
        )
        changed = True
        print(path.name, "removed portrait join")
    if "querySelectorAll('.burden-map" not in text and INNER in text:
        text = text.replace(INNER, INNER + WIPE, 1)
        changed = True
        print(path.name, "added wipe")
    if changed:
        path.write_text(text, encoding="utf-8")
        print(path.name, "wrote", path.stat().st_size)
    else:
        print(path.name, "already clean")


if __name__ == "__main__":
    for name in ("index.html", "hcc-simulator.html"):
        p = Path(name)
        if p.exists():
            patch(p)
        else:
            print(name, "missing")
