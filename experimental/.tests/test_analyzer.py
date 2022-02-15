from helpers import ROOT_PATH
from pathlib import Path

import re
from tree_sitter import Language, Parser, Tree, Node
from syntax.analyzer import Analyzer, Config, parse_config

TEST_PATTERN = r"^\s*(#)\s+([<^]-)\s*(\S+)"

class MatcherTest:
    def __init__(self, text: str):
        lines = text.splitlines()
        self.cases = []
        current_line, current_row = None, None
        for row, line in enumerate(lines):
            match = re.match(TEST_PATTERN, line) if row > 0 else None
            if not match:
                current_line, current_row = line, row
                continue
            column = match.start(2) if match.group(2)[0] == "^" else match.start(1)
            traits = match.group(3).split(",")
            self.cases.append((
                (current_row, column),
                traits if traits != ["nothing"] else [],
                current_line))
            
    def run(self, text: str, analyzer: Analyzer):
        for cursor, trait_names, line_text in self.cases:
            results = analyzer.get_scopes(text, cursor)
            if not set(results.keys()) == set(trait_names):
                print(line_text)
                print(f"location: {cursor} expected: {set(trait_names)} actual: {results.keys()}")

# Language.build_library(
#     "build/languages.dll",
#     [
#         "tree-sitter-python"
#     ]
# )

PYTHON_LANGUAGE = Language("../build/languages.dll", "python")

with open(ROOT_PATH / "config" / "python.toml", "r") as f:
    config = parse_config(f)
    analyzer = Analyzer(PYTHON_LANGUAGE, config)

with open(ROOT_PATH / ".tests" / "example.py", "r") as f:
    text = f.read()
    harness = MatcherTest(text)

harness.run(text, analyzer)