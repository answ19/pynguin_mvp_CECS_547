import argparse
import inspect
import os
import json
from pathlib import Path
from .analysis import load_module, discover_targets, TestCluster
from .search_random import generate_random_suite
from .exporter_pytest import export_pytest
from .exec_cov import exec_test_case, total_executable_lines


def main():
    ap = argparse.ArgumentParser(description="Pynguin-MVP: Automated Unit Test Generation Tool")
    ap.add_argument("--project-path", required=True)
    ap.add_argument("--module-name", required=True)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--output-path", default="out", help="Directory or file path to save generated tests")
    ap.add_argument("--debug", action="store_true", help="Print debug info")
    args = ap.parse_args()

    # --- Load module and discover targets ---
    mod = load_module(args.project_path, args.module_name)
    targets = discover_targets(mod)
    if not targets:
        print("No functions discovered.")
        return
    cluster = TestCluster(mod, targets)

    # --- Generate tests ---
    suite, hits = generate_random_suite(cluster, iters=args.iters, seed=args.seed)

    # --- Determine where to write output ---
    out_path = args.output_path
    if os.path.isdir(out_path) or out_path.endswith(os.sep):
        out_file = os.path.join(out_path, "test_generated.py")
    else:
        out_file = out_path

    out_file = export_pytest(suite, out_file)
    print(f"✅ kept {len(suite.cases)} test(s); covered {len(hits)} line hits")

    # --- Coverage summary ---
    total_lines = total_executable_lines(targets)
    covered_lines = {ln for (_fn, ln) in hits}
    covered_in_total = covered_lines & total_lines if total_lines else covered_lines
    percent = round((len(covered_in_total) / len(total_lines)) * 100, 2) if total_lines else 0.0

    print(f"📝 wrote {out_file}")
    print(f"📊 Coverage: {len(covered_in_total)} / {len(total_lines)} lines ({percent}%)")

    # --- Write JSON report ---
    out_dir = Path(args.output_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "coverage.json"
    report = {
        "module": args.module_name,
        "tests_kept": len(suite.cases),
        "covered_lines": len(covered_in_total),
        "total_lines": len(total_lines),
        "percent": percent,
        "seed": args.seed,
        "iters": args.iters,
        "output_file": str(out_file),
    }
    report_path.write_text(json.dumps(report, indent=2))
    print(f"🧾 wrote {report_path}")


if __name__ == "__main__":
    main()

