import os, inspect

def _resolve_file(target_file: str | None, module_name: str | None):
    if target_file:
        return os.path.abspath(target_file)
    if module_name:
        try:
            mod = __import__(module_name)
            path = inspect.getsourcefile(mod) or getattr(mod, "__file__", None)
            if path:
                return os.path.abspath(path)
        except Exception:
            pass
    return None

def exec_test_case(tc_code: str, globals_dict: dict, target_file: str | None, module_name: str | None) -> set[tuple[str,int]]:
    """
    Execute code and return {(abs_filename, lineno), ...} using coverage.py.
    Only lines from the target module file are returned.
    Falls back to Python's 'trace' if coverage isn't available.
    """
    filename = _resolve_file(target_file, module_name)

    # --- Preferred: coverage.py
    try:
        import coverage  # type: ignore
        cov = coverage.Coverage(
            include=[filename] if filename else None,
            branch=False,
        )
        cov.start()
        try:
            exec(tc_code, globals_dict, globals_dict)
        except Exception:
            pass
        finally:
            cov.stop()
        hits: set[tuple[str,int]] = set()
        data = cov.get_data()
        for fn in data.measured_files():
            # accept exact file or same basename (robust to path differences)
            if filename:
                if os.path.abspath(fn) != filename and os.path.basename(fn) != os.path.basename(filename):
                    continue
            for ln in (data.lines(fn) or []):
                hits.add((os.path.abspath(fn), int(ln)))
        return hits
    except Exception:
        # --- Fallback: trace module
        import trace
        tracer = trace.Trace(count=True, trace=False, ignoremods=set(), ignoredirs=[])
        try:
            tracer.runctx(tc_code, globals_dict, globals_dict)
        except Exception:
            pass
        results = tracer.results()
        counts = getattr(results, "counts", {})
        hits: set[tuple[str,int]] = set()
        for fn, lineno_map in counts.items() if isinstance(counts, dict) else []:
            fn_abs = os.path.abspath(fn)
            if filename:
                if fn_abs != filename and os.path.basename(fn_abs) != os.path.basename(filename):
                    continue
            # lineno_map is a dict {lineno: count}
            for ln in (lineno_map.keys() if hasattr(lineno_map, "keys") else []):
                hits.add((fn_abs, int(ln)))
        return hits

# Helper used by CLI for % summary
def total_executable_lines(targets: list[dict]) -> set[int]:
    totals: set[int] = set()
    for t in targets:
        obj = t.get("obj")
        if obj is None:
            continue
        try:
            src, start = inspect.getsourcelines(obj)
            totals |= set(range(start, start + len(src)))
        except (OSError, TypeError):
            continue
    return totals
