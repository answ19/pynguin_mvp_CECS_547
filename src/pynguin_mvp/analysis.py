import importlib, inspect, sys
from typing import Any, get_type_hints

def load_module(project_path: str, module_name: str):
    if project_path not in sys.path:
        sys.path.insert(0, project_path)
    return importlib.import_module(module_name)

def discover_targets(mod) -> list[dict[str, Any]]:
    """Return top-level functions with signature & type hints."""
    targets: list[dict[str, Any]] = []
    for name, obj in inspect.getmembers(mod):
        if inspect.isfunction(obj) and not name.startswith("_"):
            try:
                hints = get_type_hints(obj)
            except Exception:
                hints = {}
            sig = inspect.signature(obj)
            targets.append({"name": name, "obj": obj, "sig": sig, "hints": hints})
    return targets

class TestCluster:
    def __init__(self, module, targets: list[dict[str, Any]]):
        self.module = module
        self.targets = targets
