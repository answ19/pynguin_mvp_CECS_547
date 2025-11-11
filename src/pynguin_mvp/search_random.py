from .ir import Statement, TestCase, TestSuite
from .generators import build_args
from .exec_cov import exec_test_case
import random, numbers, os, inspect

def _resolve_source_path(module) -> str | None:
    path = inspect.getsourcefile(module) or getattr(module, "__file__", None)
    return os.path.abspath(path) if path else None

def _num_required_positional_params(sig):
    n = 0
    for p in sig.parameters.values():
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) and p.default is p.empty:
            n += 1
    return n

def _maybe_append_assertion(tc, g):
    if "res" in g:
        v = g["res"]
        if isinstance(v, (str, bool, numbers.Number)):
            tc.statements.append(Statement(code=f"assert res == {v!r}"))

def _emit_call(name, *args):
    parts = []
    for i, v in enumerate(args):
        parts.append(f"arg_{i} = {repr(v)}")
    call = f"res = mod.{name}({', '.join(f'arg_{i}' for i in range(len(args)))})"
    return [Statement(code=c) for c in parts] + [Statement(code=call)]

def _triangle_scenarios(func_name: str):
    # Deterministic, labeled examples for triangle.classify
    return [
        ("boundary", _emit_call(func_name, 1, 1, 1)),        # equilateral (lower positive boundary)
        ("invalid",  _emit_call(func_name, 1, 2, 9)),        # violates triangle inequality
        ("boundary", _emit_call(func_name, 10, 10, 7)),      # isosceles, valid boundary-ish
        ("boundary", _emit_call(func_name, 6, 3, 7)),        # scalene, valid
        ("invalid",  _emit_call(func_name, 0, 5, 5)),        # non-positive side
    ]

def generate_random_suite(cluster, iters=200, seed=None):
    if seed is not None:
        random.seed(seed)

    suite = TestSuite(target_module=cluster.module.__name__)
    g = {}
    header = f"import {cluster.module.__name__} as mod\n"
    module_name = cluster.module.__name__

    # Bootstrap: ensure at least one executed call
    t0 = cluster.targets[0]
    npos = _num_required_positional_params(t0["sig"])
    safe_args = ", ".join(["1"] * npos) if npos > 0 else ""
    boot_tc = TestCase([Statement(code=f"res = mod.{t0['name']}({safe_args})")], label="bootstrap")
    boot_hits = exec_test_case(header + boot_tc.emit_py(), g, None, module_name)
    seen = set()
    if boot_hits:
        _maybe_append_assertion(boot_tc, g)
        suite.cases.append(boot_tc)
        seen |= boot_hits
    else:
        suite.cases.append(boot_tc)  # keep one test so pytest runs

    # Deterministic scenario tests (use cases)
    # You can branch on module/function name here if you add more targets in the future.
    if t0["name"] == "classify" and cluster.module.__name__ == "triangle":
        for label, stmts in _triangle_scenarios(t0["name"]):
            tc = TestCase(stmts, label=label)
            hits = exec_test_case(header + tc.emit_py(), g, None, module_name)
            if hits - seen:
                _maybe_append_assertion(tc, g)
                suite.cases.append(tc)
                seen |= hits

    # Random loop: keep tests that add new coverage
    k = len(cluster.targets)
    for i in range(iters):
        t = cluster.targets[i % k]
        args_code, arg_names = build_args(t["sig"], t["hints"])
        call_code = f"res = mod.{t['name']}({', '.join(arg_names)})"
        tc = TestCase([*(Statement(code=c) for c in args_code), Statement(code=call_code)], label="random")
        hits = exec_test_case(header + tc.emit_py(), g, None, module_name)
        if hits - seen:
            _maybe_append_assertion(tc, g)
            suite.cases.append(tc)
            seen |= hits

    return suite, seen

