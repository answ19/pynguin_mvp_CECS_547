import sys, os, inspect
from types import FrameType

class LineTracer:
    def __init__(self, module_name: str | None):
        # only match by basename, e.g., "triangle.py"
        self.want_base = f"{module_name}.py" if module_name else None
        self.hits: set[tuple[str,int]] = set()

    def tracer(self, frame: FrameType, event: str, arg):
        if event == "line":
            base = os.path.basename(frame.f_code.co_filename.replace("\\", "/"))
            if self.want_base is None or base == self.want_base:
                self.hits.add((os.path.abspath(frame.f_code.co_filename), frame.f_lineno))
        return self.tracer

def exec_test_case(tc_code: str, globals_dict: dict, _target_file_unused, module_name: str | None) -> set[tuple[str,int]]:
    tracer = LineTracer(module_name)
    sys.settrace(tracer.tracer)
    try:
        exec(tc_code, globals_dict, globals_dict)
    except Exception:
        pass
    finally:
        sys.settrace(None)
    return tracer.hits

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

