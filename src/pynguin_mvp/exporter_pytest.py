from pathlib import Path
from .ir import TestSuite
import os

def export_pytest(suite: TestSuite, out_dir: str, project_path: str | None = None):
    p = Path(out_dir); p.mkdir(parents=True, exist_ok=True)
    out = p / "test_generated.py"
    with out.open("w") as f:
        if project_path:
            f.write("import sys, os\n")
            f.write(f"sys.path.insert(0, {project_path!r})\n")
        f.write(f"import {suite.target_module} as mod\n")
        for i, tc in enumerate(suite.cases):
            f.write(f"def test_case_{i}():\n")
            f.write(tc.emit_py())
            f.write("\n")
    return str(out)
