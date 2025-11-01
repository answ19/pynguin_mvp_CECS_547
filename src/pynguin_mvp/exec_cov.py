import os, inspect, sys

def _debug(msg: str):
    if os.environ.get("PYNGUIN_DEBUG") == "1":
        print(f"[pynguin-mvp] {msg}")

def exec_test_case(tc_code: str, globals_dict: dict, target_file: str | None, module_name: str | None) -> set[tuple[str,int]]:
    """
    Execute code and return {(abs_filename, lineno), ...}.
    Strategy:
      1) Try coverage.py (no include filter). After run, keep only files whose
         basename matches f"{module_name}.py".
      2) If coverage returns no hits for that file, fall back to trace.Trace.
    """
    want_base = f"{module_name}.py" if module_name else None
    hits: set[tuple[str,int]] = set()

    # --- Preferred: coverage.py ---
    try:
        import coverage  # type: ignore
        cov = coverage.Coverage(branch=False)
        cov.start()
        try:
            exec(tc_code, globals_dict, globals_dict)
        except Exception:
            # swallow test generation failures in MVP
            pass
        finally:
            cov.stop()

        data = cov.get_data()
        files = [os.path.abspath(f) for f in data.measured_files()]
        _debug(f"coverage measured_files: {files}")
        for fn in files:
            fn_abs = os.path.abspath(fn)
            if want_base is None or os.path.basename(fn_abs) == want_base:
                for ln in (data.lines(fn) or []):
                    hits.add((fn_abs, int(ln)))

        if hits:
            return hits
    except Exception as e:
        _debug(f"coverage failed: {e!r}")

    # --- Fallback: trace module (more permissive) ---
    try:
        import trace
        tracer = trace.Trace(count=True, trace=False)
        try:
            tracer.runctx(tc_code, globals_dict, globals_dict)
        except Exception:
            pass
        results = tracer.results()
        counts = getattr(results, "counts", None)
        if isinstance(counts, dict):
            for fn, lineno_map in counts.items():
                fn_abs = os.path.abspath(fn)
                if want_base is None or os.path.basename(fn_abs) == want_base:
                    for ln in getattr(lineno_map, "keys", lambda: [])():
                        hits.add((fn_abs, int(ln)))
    except Exception as e:
        _debug(f"trace fallback failed: {e!r}")

    return hits

# Helper for CLI % summary
def total_executable_lines(targets: list[dict]) -> set[int]:
    totals: set[int] = set()
    for t in targets:
        obj = t.get("obj")
        if obj is None:
            continue
    # include full function bodies discovered
        try:
            src, start = inspect.getsourcelines(obj)
            totals |= set(range(start, start + len(src)))
        except (OSError, TypeError):
            continue
    return totals
