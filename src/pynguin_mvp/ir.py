from dataclasses import dataclass, field

@dataclass
class Statement:
    code: str  # e.g., "x = 3"

@dataclass
class TestCase:
    def __init__(self, statements):
        self.statements = statements  # list[Statement]

    def emit_py(self) -> str:
        # IMPORTANT: emit raw, executable statements for search-time exec()
        return "".join(s.code.rstrip() + "\n" for s in self.statements)

@dataclass
class TestSuite:
    target_module: str
    cases: list[TestCase] = field(default_factory=list)
