import os

def _indent(code: str, spaces: int = 4) -> str:
    pad = " " * spaces
    out_lines = []
    for ln in code.splitlines(True):
        if ln.strip():
            out_lines.append(pad + ln.lstrip())
        else:
            out_lines.append(ln)
    if not out_lines or not out_lines[-1].endswith("\n"):
        out_lines.append("\n")
    return "".join(out_lines)

def export_pytest(suite, out_path: str) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    header = (
        "import sys, os\n"
        "sys.path.insert(0, '.')\n"
        f"import {suite.target_module} as mod\n\n"
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
        for i, tc in enumerate(suite.cases):
            label = getattr(tc, "label", "random")
            f.write(f"def test_{label}_{i}():\n")
            f.write(_indent(tc.emit_py(), 4))
            f.write("\n")
    return out_path

