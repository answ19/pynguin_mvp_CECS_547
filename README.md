🧪 Pynguin-MVP — Automated Unit Test Generation for Python

A lightweight re-implementation of the core concepts from the research tool Pynguin: Automated Unit Test Generation for Python (Lukasczyk et al., ICSE 2021).
This project automatically analyzes Python code, generates tests, measures coverage, and produces a clear pytest suite and HTML report — all in pure Python.

🚀 Features

🔍 Automatic Test Discovery: identifies functions and parameters via reflection (inspect).
🎲 Random Test Generation: produces diverse test inputs guided by type hints.
📈 Coverage-Guided Selection: retains only tests that add new line coverage.
🧾 Regression Assertions: automatically inserts assert res == <value>.
⚙️ Pytest Exporter: writes runnable out/test_generated.py.
🌐 HTML Report: generates out/report.html with coverage summary, progress bar, and full test code.
🧩 Multiple Use Cases: labeled scenarios — boundary, invalid, random, bootstrap — with counts shown in the HTML “Use Cases” table.
💡 Educational & Lightweight: minimal dependencies; demonstrates search-based test generation concepts clearly.

🧰 Project Structure

```plaintext
pynguin_mvp/
├── src/
│   └── pynguin_mvp/
│       ├── analysis.py
│       ├── ir.py
│       ├── generators.py
│       ├── exec_cov.py
│       ├── search_random.py
│       ├── exporter_pytest.py
│       └── cli.py
│
├── scripts/
│   └── make_report.py          # Builds out/report.html
│
├── out/
│   ├── test_generated.py
│   ├── coverage.json
│   └── report.html
│
├── triangle.py                 # Sample target module
├── screenshots/                # Images for PDF/report
├── report_final.pdf
└── README.md

```
💻 Installation

#1 Clone or open project
cd /mnt/c/Users/anuja/pynguin_mvp

#2 create & activate virtual environment
python -m venv .venv
source .venv/bin/activate

#3 install dependencies
pip install -e .
pip install pytest coverage reportlab

🧩 Usage
#Generate tests for triangle.py
pynguin-mvp --project-path . --module-name triangle --iters 200 --seed 7 --output-path ./out

#Run generated tests
pytest -q out/test_generated.py

#View coverage JSON
cat out/coverage.json

#Build HTML report
python scripts/make_report.py out

📂 Open out/report.html in your browser for a full visual summary.

📊 Example Output
✅ kept 4 test(s); covered 8 line hits
📊 Coverage: 8 / 10 lines (80.0%)
🧾 wrote out/coverage.json
✅ Wrote out/report.html


Sample generated test:

def test_boundary_1():
    arg_a = 6
    arg_b = 3
    arg_c = 7
    res = mod.classify(arg_a, arg_b, arg_c)
    assert res == 'scalene'

🌐 HTML Report Preview

Includes:
Coverage badge + progress bar
“Use Cases” summary table
Download button for test_generated.py
Syntax-highlighted test code

🧠 Results Summary
```
| Metric               | Result                                  |
| -------------------- | --------------------------------------- |
| Functions discovered | 1 (`classify`)                          |
| Tests generated      | 4                                       |
| Lines covered        | 8 / 10                                  |
| **Coverage**         | **80 %**                                |
| Labels               | boundary / invalid / random / bootstrap |
| Pytest               | ✅ All tests passed                      |

```

🔬 Comparison with Original Pynguin
```
| Feature           | Pynguin (Research Tool)                | Pynguin-MVP (This Project)                |
| ----------------- | -------------------------------------- | ----------------------------------------- |
| Algorithms        | DynaMOSA / Whole-Suite / Random        | Random + coverage feedback                |
| Dependencies      | Heavy (Java bridge + analysis engines) | Pure Python, lightweight                  |
| Front-End         | CLI only                               | CLI + HTML report                         |
| Test Labels       | None                                   | ✅ boundary / invalid / random / bootstrap |
| Educational Value | Hard to set up                         | Easy to explain & extend                  |
| Target            | Research benchmarking                  | Teaching / demo tool                      |
| Example Result    | High coverage                          | **80 % coverage on triangle.py**          |
```

🧩 Future Enhancements
Add branch coverage and mutation testing.

Integrate subprocess sandboxing for untrusted code.

Add Streamlit UI to visualize multiple modules.

Extend use-case labeling for other target functions.

🧾 References

Lukasczyk et al., “Pynguin: Automated Unit Test Generation for Python,” ICSE 2021.
Original Pynguin GitHub
Python Docs — inspect, trace, coverage, pytest

👩‍💻 Author

Anuja Sawant
Computer Science Graduate Student – CECS 547 Software Maintenance and Reengineering and Reuse © 2025 Pynguin-MVP Project

✅ Summary

Pynguin-MVP successfully reproduces the core principles of automated test generation while improving on:
Usability: simple CLI, no heavy dependencies.
Visualization: clear HTML report.
Interpretability: labeled test cases for multiple use-case categories.
Coverage: 80 % on sample module with 4 passing tests.
