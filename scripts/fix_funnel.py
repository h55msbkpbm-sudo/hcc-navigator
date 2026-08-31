#!/usr/bin/env python3
from pathlib import Path
import re

QFLOW_NEW = """const QFLOW = [
  { g:0, key:'mvi', group:'Disease', h:'Macrovascular invasion', lead:'Vp0-Vp4, or hepatic vein / IVC, on the current staging scan.' },
  { g:0, key:'ehs', group:'Disease', h:'Extrahepatic spread', lead:'Nodes or distant metastases.' },
  { g:1, key:'ecog', group:'Fitness', h:'ECOG performance status' },
  { g:1, key:'liver', group:'Fitness', h:'Child-Pugh class', lead:'Current liver function.' },
  { g:2, key:'varices', group:'Safety', h:'Oesophageal varices' },
  { g:2, key:'egd', group:'Safety', h:'OGD within 6 months', lead:'Required before atezolizumab + bevacizumab (HA HAB-P365).' },
  { g:2, key:'cardioFactors', group:'Safety', h:'Cardiovascular / anti-VEGF safety', lead:'Select all that apply. High CV risk blocks bevacizumab.' },
  { g:2, key:'autoimmuneFactors', group:'Safety', h:'Autoimmune / IO safety', lead:'Select all that apply. Active autoimmune blocks the IO pathway.' }
];"""

FOUC_RE = re.compile(r"\s*<script>\s*\(function \(\) \{.*?</script>", re.S)

def patch(s):
    notes = []
    s2, n = re.subn(r"const QFLOW = \[.*?\];", QFLOW_NEW, s, count=1, flags=re.S)
    if n:
        s = s2
        notes.append("qflow")
    s2, n = re.subn(
        r'<div class="step-label">1 of 10</div>\s*<h1>Number of intrahepatic lesions</h1>\s*<p class="lead">Count discrete enhancing nodules[^<]*</p>',
        '<div class="step-label">1 of 8</div>\n        <h1>Macrovascular invasion</h1>\n        <p class="lead">Vp0-Vp4, or hepatic vein / IVC, on the current staging scan.</p>',
        s, count=1)
    if n:
        s = s2
        notes.append("first-paint-10")
    if FOUC_RE.search(s):
        s = FOUC_RE.sub("", s, count=1)
        notes.append("fouc")
    s2, n = re.subn(
        r'(id="step0">\s*<div class="step-label">)1 of \d+(</div>\s*<h1>)[^<]+(</h1>\s*<p class="lead">)[^<]*',
        r"\g<1>1 of 8\g<2>Macrovascular invasion\g<3>Vp0-Vp4, or hepatic vein / IVC, on the current staging scan.",
        s, count=1)
    if n:
        s = s2
        notes.append("first-paint")
    s = s.replace('<div class="card q-on">', '<div class="card">')
    s = s.replace(
        '<div class="card">\n          <h3><span class="qnum">1</span> Macrovascular invasion</h3>',
        '<div class="card q-on">\n          <h3><span class="qnum">1</span> Macrovascular invasion</h3>')
    s = s.replace(
        '<div class="card">\n          <h3><span class="qnum">3</span> Macrovascular invasion</h3>',
        '<div class="card q-on">\n          <h3><span class="qnum">1</span> Macrovascular invasion</h3>')
    notes.append("q-on")
    old_a = "['age','sex','viral','metabolic','cirrhosis','afp','cardioFactors','autoimmuneFactors']"
    old_b = "['age','sex','viral','metabolic','cirrhosis','afp']"
    new_k = "['age','sex','viral','metabolic','cirrhosis','afp','lesions','largest']"
    if old_a in s:
        s = s.replace(old_a, new_k, 1)
        notes.append("reloc-a")
    elif old_b in s:
        s = s.replace(old_b, new_k, 1)
        notes.append("reloc-b")
    if "['albiCard','pagebCard']" in s:
        s = s.replace("['albiCard','pagebCard']", "['albiCard','pagebCard','burdenCalcCard']", 1)
        notes.append("burden-adv")
    s = s.replace(
        "Age, sex, etiology, and AFP \u2014 annotation only. They do not switch A+B vs STRIDE.",
        "Age, sex, etiology, AFP, lesion count, and size \u2014 annotation only. They do not switch A+B vs STRIDE.")
    s2, n = re.subn(
        r"\n    \$\{row\('gap', 'Systemic-discussable uHCC \(BCLC-B/C band\)', F\.systemicModelled, null, 'modelled', false\)\}",
        "", s, count=1)
    if n:
        s = s2
        notes.append("drop-503-row")
    s = s.replace(
        "~503 is <strong>MODELLED/GAP</strong> \u2014 not a registry count.",
        "Unresectable / IO / VEGF volumes are not published by HKCaR.")
    if "~503 scale" in s:
        s = s.replace(
            "All other inputs MODELLED. Not epidemiology. Scaled headcount uses ~503 MODELLED/GAP only.",
            "All other inputs MODELLED. Not epidemiology. No invented caseload headcount.")
        s = s.replace(
            '<thead><tr><th>Output</th><th>%</th><th>~503 scale</th></tr></thead>',
            '<thead><tr><th>Output</th><th>%</th></tr></thead>')
        s = s.replace("<td>21.8</td><td>110</td>", "<td>21.8</td>")
        s = s.replace("<td>37.2</td><td>187</td>", "<td>37.2</td>")
        s = s.replace("<td>23.1</td><td>116</td>", "<td>23.1</td>")
        s = s.replace("<td>7.1</td><td>36</td>", "<td>7.1</td>")
        s = s.replace("<td>10.8</td><td>54</td>", "<td>10.8</td>")
        s = s.replace("<td>0</td><td>0</td>", "<td>0</td>")
        s = s.replace("<td>41.1</td><td>\u2014</td>", "<td>41.1</td>")
        s = s.replace("<td>89.2</td><td>\u2014</td>", "<td>89.2</td>")
        s = s.replace("<td>0</td><td>\u2014</td>", "<td>0</td>")
        notes.append("drop-503-scale")
    if "const htmlOut = matchLead + recLead +" in s:
        s = s.replace(
            'const htmlOut = matchLead + recLead +\n    `<details class="mdt-fold" id="res-details"><summary>Details</summary><div class="fold-body">${designLead}',
            'const htmlOut = recLead +\n    `<details class="mdt-fold" id="res-details"><summary>Details</summary><div class="fold-body">${matchLead}${designLead}',
            1)
        notes.append("rec-first")
    return s, notes

def main():
    for name in ("index.html", "hcc-simulator.html"):
        p = Path(name)
        if not p.exists():
            print("skip", name)
            continue
        raw = p.read_text(encoding="utf-8")
        out, notes = patch(raw)
        if out != raw:
            p.write_text(out, encoding="utf-8")
        q = re.search(r"const QFLOW = \[(.*?)\];", out, re.S)
        keys = re.findall(r"key:'([^']+)'", q.group(1) if q else "")
        print(name, "notes=", notes, "keys=", keys, "n=", len(keys))
        assert keys == ["mvi", "ehs", "ecog", "liver", "varices", "egd", "cardioFactors", "autoimmuneFactors"], keys
        assert "function decide()" in out
        assert "Systemic-discussable uHCC" not in out

if __name__ == "__main__":
    main()
