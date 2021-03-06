import toml
from typing import Iterator
from dataclasses import dataclass
from tree_sitter import Language, Parser, Tree, Node

@dataclass
class Pattern:
    target_tags: list[str]
    next_tags: list[str]
    commands: list[str]
    query: str

@dataclass
class Config:
    sentinel: str
    matcher: dict[str, Pattern]
    
@dataclass
class MatchInfo:
    start_point: tuple[int, int]
    end_point: tuple[int, int]
    text: str
    placeholder: bool
    commands: list[str]
    score: int

    def make_placeholder(node: Node):
        return MatchInfo(
            node.start_point,
            node.start_point,
            "$0",
            True,
            [],
            MatchInfo._score_node(node)
        )
    
    def make_match(node: Node, commands: list[str]):
        return MatchInfo(
            node.start_point,
            node.end_point,
            node.text.decode("utf8"),
            False,
            commands,
            MatchInfo._score_node(node)
        )
    
    def _score_node(node: Node):
        score = 0
        while node:
            score += 1
            node = node.parent
        return score

class Matcher:
    def __init__(self, query):
        self.query = query
        
    def matches(self, root: Node, cursor: tuple[int, int]) -> Iterator[Node]:
        return self._process_matches(self.query.captures(root), cursor)

    def _process_matches(self, captures: list[tuple[Node, str]], cursor: tuple[int, int]) -> Iterator[Node]:
        def overlaps_cursor(node: Node):
            return node.start_point <= cursor and node.end_point >= cursor                
                
        target = None
        included = False
        for capture in captures:
            node, label_text = capture
            labels = label_text.split("-")

            # Captures go in sequence of in-order traversal of the syntax tree.
            # This means that excludes will always occur after parent includes.
            # Match directives are required to be ancestors of all other labels,
            # so they will always come first.
            # This means we can simply process captures in turn.
            if "match" in labels:
                if included and target:
                    yield target
                target = None
                included = False
            if "target" in labels:
                # target = node if node.text else target
                target = node
            if "include" in labels:
                included = included or overlaps_cursor(node)
            if "exclude" in labels:
                included = included and not overlaps_cursor(node)

        if included and target:
            yield target

def merge_matches(result: dict[str, MatchInfo], source: dict[str, MatchInfo]):
    for tag, node in source.items():
        if tag in result:
            result[tag] = max(result[tag], node, key=lambda n: n.score)
        else:
            result[tag] = node        

class Scanner:
    def __init__(self, lang: Language, patterns: dict[str, Pattern]):
        self.patterns = patterns
        self.matchers = {
            key: Matcher(lang.query(value.query)) for key, value in patterns.items()
        }
    
    def matches(self, root: Node, cursor: tuple[int, int], sentinel: str):
        result: dict[str, Node] = {}                
        for name, matcher in self.matchers.items():
            for node in matcher.matches(root, cursor):
                if sentinel:
                    if node.text.decode("utf8") != sentinel:
                        continue
                    node = MatchInfo.make_placeholder(node)
                else:
                    node = MatchInfo.make_match(node, self.patterns[name].commands)                        
                    
                tags = self.patterns[name].target_tags if sentinel else self.patterns[name].next_tags
                merge_matches(result, {tag: node for tag in tags})

        return result            

class Analyzer:
    def __init__(self, lang: Language, config: Config):
        self.parser = Parser()
        self.parser.set_language(lang)
        self.scanner = Scanner(lang, config.matcher)
        self.sentinel = config.sentinel

    def get_scopes(self, text: str, cursor: tuple[int, int]):
        text = Analyzer.normalize(text)
        tree = self.parser.parse(text.encode("utf8"))
        results = self.scanner.matches(tree.root_node, cursor, None)

        tree = self.parser.parse(self.insert_sentinel(text, cursor).encode("utf8"))
        results_next = self.scanner.matches(tree.root_node, cursor, self.sentinel)
        
        merge_matches(results, results_next)
        return results        
    
    def normalize(text: str) -> str:
        return text.replace("\r\n", "\n")
        
    def insert_sentinel(self, text: str, cursor: tuple[int, int]):
        row, column = cursor
        lines = text.splitlines()
        line = lines[row]
        line = line[:column] + self.sentinel + line[column:]
        lines[row] = line
        return "\n".join(lines)

def parse_config(f) -> Config:
    d = toml.load(f)
    return Config(
        d["sentinel"],
        { key: Pattern(
            value["target_tags"] if "target_tags" in value else [], 
            value["next_tags"] if "next_tags" in value else [],
            value["commands"] if "commands" in value else [],
            value["query"]
        ) for key, value in d["matcher"].items() }
    )