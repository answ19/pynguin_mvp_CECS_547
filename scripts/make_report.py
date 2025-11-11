import json, os, html, datetime, sys

def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def badge(percent: float) -> str:
    color = "#e74c3c"
    if percent >= 80: color = "#2ecc71"
    elif percent >= 50: color = "#f1c40f"
    return f'<span style="background:{color};color:white;padding:4px 8px;border-radius:6px;font-weight:600">{percent:.1f}%</span>'

def progress(percent: float) -> str:
    pct = max(0, min(100, percent))
    return f'''
<div style="background:#eee;border-radius:10px;height:14px;width:260px;overflow:hidden">
  <div style="height:100%;width:{pct:.1f}%;background:#4f46e5"></div>
</div>'''

def _labels_table(labels: dict) -> str:
    if not labels:
        return "<div class='muted'>No labels reported.</div>"
    rows = "\n".join(
        f"<tr><td>{html.escape(k)}</td><td style='text-align:right'><b>{v}</b></td></tr>"
        for k, v in sorted(labels.items())
    )
    return f"""
<table style="width: 320px; border-collapse: collapse">
  <thead>
    <tr><th style="text-align:left;border-bottom:1px solid #e5e7eb">Use case</th>
        <th style="text-align:right;border-bottom:1px solid #e5e7eb">Tests</th></tr>
  </thead>
  <tbody>
    {rows}
  </tbody>
</table>"""

def main(out_dir: str = "out"):
    cov_path = os.path.join(out_dir, "coverage.json")
    test_path = os.path.join(out_dir, "test_generated.py")
    report_path = os.path.join(out_dir, "report.html")

    cov = {}
    if os.path.exists(cov_path):
        with open(cov_path, "r", encoding="utf-8") as f:
            cov = json.load(f)

    module = cov.get("module", "unknown")
    tests_kept = cov.get("tests_kept", 0)
    covered = cov.get("covered_lines", 0)
    total = cov.get("total_lines", 0)
    percent = float(cov.get("percent", 0.0))
    seed = cov.get("seed", "")
    iters = cov.get("iters", "")
    output_file = cov.get("output_file", test_path)
    labels = cov.get("labels", {})

    code = read_text(test_path)
    code_html = html.escape(code)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Pynguin-MVP Report – {html.escape(module)}</title>
<style>
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; color: #111827; }}
  h1 {{ margin: 0 0 4px; font-size: 24px; }}
  .sub {{ color:#6b7280; margin-bottom: 16px; }}
  .card {{ border:1px solid #e5e7eb; border-radius:12px; padding:16px; margin:14px 0; }}
  .row {{ display:flex; gap:16px; flex-wrap:wrap }}
  .box {{ flex:1 1 260px; }}
  .k {{ color:#6b7280 }}
  pre {{ background:#0b1021; color:#e5e7eb; padding:16px; border-radius:12px; overflow:auto; }}
  code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }}
  .muted {{ color:#6b7280; font-size: 13px; }}
  a.btn {{ display:inline-block; text-decoration:none; background:#111827; color:#fff; padding:8px 12px; border-radius:8px; }}
</style>
</head>
<body>
  <h1>Pynguin-MVP Report</h1>
  <div class="sub">Generated: {now}</div>

  <div class="card">
    <div class="row">
      <div class="box">
        <div class="k">Module</div>
        <div><b>{html.escape(module)}</b></div>
      </div>
      <div class="box">
        <div class="k">Tests kept</div>
        <div><b>{tests_kept}</b></div>
      </div>
      <div class="box">
        <div class="k">Coverage</div>
        <div style="display:flex;align-items:center;gap:10px">
          {badge(percent)}
          {progress(percent)}
          <span class="muted">{covered} / {total} lines</span>
        </div>
      </div>
      <div class="box">
        <div class="k">Search params</div>
        <div>seed=<b>{seed}</b> &nbsp; iters=<b>{iters}</b></div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2 style="margin:0 0 8px">Use Cases</h2>
    {_labels_table(labels)}
  </div>

  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
      <h2 style="margin:0">Generated Tests (pytest)</h2>
      <a class="btn" href="{html.escape(output_file)}" download>Download test_generated.py</a>
    </div>
    <pre><code>{code_html}</code></pre>
  </div>

  <div class="muted">Open this file in your browser: <code>{html.escape(report_path)}</code></div>
</body>
</html>
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_doc)

    print(f"✅ Wrote {report_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    main(out)

