from talon import Module, Context, actions, grammar
from typing import List
from functools import reduce

mod = Module()
ctx = Context()

@mod.capture(rule="({self.vocabulary} | <word>)")
def word(m) -> str:
    "Single word"
    words = capture_to_words(m)
    return words[0]

@mod.capture(rule="({self.vocabulary} | <phrase>)+")
def words(m) -> str:
    "Multiple words"
    return " ".join(capture_to_words(m))
    
def capture_to_words(m):
    def parse(w):
        if isinstance(w, grammar.vm.Phrase):
            return actions.dictate.replace_words(actions.dictate.parse_words(w))
        return w.split(" ")
    return reduce(lambda x, y: x + y, map(parse, m))

@mod.action_class
class Actions:
    def insert_many(strings: List[str]) -> None:
        "Insert multiple strings"
        for string in strings:
            actions.insert(string)
    def insert_formatted(text: str, format: str) -> None:
        "Insert formatted"
        actions.insert(actions.user.format_text(text, format))