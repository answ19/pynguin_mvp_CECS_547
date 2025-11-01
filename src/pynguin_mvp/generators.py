import random, string, inspect, typing

def gen_int(): return random.randint(1, 10)
def gen_float(): return random.uniform(-10.0, 10.0)
def gen_str(n: int = 5): return "".join(random.choice(string.ascii_lowercase) for _ in range(n))
def gen_bool(): return random.choice([True, False])
def gen_list(elem_gen, n: int = 3): return [elem_gen() for _ in range(random.randint(0, n))]

def _for_builtin(t):
    return {
        int: gen_int,
        float: gen_float,
        str: gen_str,
        bool: gen_bool,
        list: lambda: gen_list(gen_int),
    }.get(t)

def pick_generator(py_type):
    """Pick a generator function based on annotations (Python 3.11+ features OK)."""
    if py_type is None:
        return gen_int
    g = _for_builtin(py_type)
    if g: return g

    origin = typing.get_origin(py_type)
    args = typing.get_args(py_type)
    if origin is list and args:
        elem_t = args[0]
        elem_gen = pick_generator(elem_t)
        return lambda: gen_list(elem_gen)
    # Fallbacks
    return gen_int

def build_args(sig: inspect.Signature, hints: dict):
    args_code: list[str] = []
    arg_names: list[str] = []
    for i, (pname, param) in enumerate(sig.parameters.items()):
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        hinted = hints.get(pname)
        gen = pick_generator(hinted)
        var = f"arg_{pname or i}"
        val = gen()
        args_code.append(f"{var} = {val!r}")
        arg_names.append(var)
    return args_code, arg_names
