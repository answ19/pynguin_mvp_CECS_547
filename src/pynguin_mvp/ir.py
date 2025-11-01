from dataclasses import dataclass, field

@dataclass
class Statement:
    code: str  # e.g., "x = 3"

@dataclass
class TestCase:
    statements: list[Statement] = field(default_factory=list)

    def emit_py(self, indent: str = "    ") -> str:
        return "".join(f"{indent}{s.code}\n" for s in self.statements)

@dataclass
class TestSuite:
    target_module: str
    cases: list[TestCase] = field(default_factory=list)
