import argparse, inspect, os, json
from pathlib import Path
from .analysis import load_module, discover_targets, TestCluster
from .search_random import generate_random_suite
from .exporter_pytest import export_pytest
from .exec_cov import exec_test_case, total_executable_lines

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-path", required=True)
    ap.add_argument("--module-name", required=True)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--output-path", default="out")
    ap.add_argument("--timeout", type=float, default=2.0, help="Per-test timeout in seconds (sandbox only).")
    ap.add_argument("--sandbox", action="store_true", help="Run each candidate test in a subprocess with a timeout.")
    ap.add_argument("--debug", action="store_true",
                    help="Run one traced call to the first function and print raw coverage hits.")
    args = ap.parse_args()

    mod = load_module(args.project_path, args.module_name)
    targets = discover_targets(mod)
    if not targets:
        print("No functions discovered.")
        return
    cluster = TestCluster(mod, targets)

    if args.debug:
        t = targets[0]
        header = f"import {cluster.module.__name__} as mod\n"
        body = f"res = mod.{t['name']}(1, 1, 1)\n"
        code = header + body
        target_file = inspect.getsourcefile(cluster.module) or getattr(cluster.module, "__file__", "")
        target_file = os.path.abspath(target_file)
        hits = exec_test_case(code, {}, target_file, cluster.module.__name__)
        print("DEBUG: target_file =", target_file)
        if hits:
            print("DEBUG: tracer hits (first 10):")
            for h in list(sorted(hits))[:10]:
                print("   ", h)
        else:
            print("DEBUG: no hits recorded")
        return

    suite, hits = generate_random_suite(
        cluster,
        iters=args.iters,
        seed=args.seed,
    )
    out_file = export_pytest(suite, args.output_path, project_path=args.project_path)
    print(f"✅ kept {len(suite.cases)} test(s); covered {len(hits)} line hits")
    print(f"📝 wrote {out_file}")

    total_lines = total_executable_lines(targets)
    covered_lines = {ln for (_fn, ln) in hits}
    covered_in_total = covered_lines & total_lines if total_lines else covered_lines
    percent = round((len(covered_in_total) / len(total_lines)) * 100, 2) if total_lines else 0.0
    print(f"📊 Coverage: {len(covered_in_total)} / {len(total_lines)} lines ({percent}%)")

    out_dir = Path(args.output_path); out_dir.mkdir(parents=True, exist_ok=True)
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
