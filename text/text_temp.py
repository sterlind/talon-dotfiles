from talon import Module, Context, actions, grammar
from typing import List
from functools import reduce

mod = Module()
ctx = Context()

@mod.capture(rule="(abbreviate|brief|abbrieve) {user.abbreviation}")
def abbreviated_word(m) -> str:
    return m.abbreviation
    
@mod.capture(rule="spell (<user.letter>)+ [over]")
def spelled_word(m) -> str:
    return "".join(m.letter_list)

@mod.capture(rule = "cap <user.unmodified_word>")
def capitalized_word(m) -> str:
    "Capitalized modifier for words (put other modifiers here)"
    return m.unmodified_word.capitalize()

@mod.capture(rule="({self.vocabulary} | <user.abbreviated_word> | <user.spelled_word> | <word>)")
def unmodified_word(m) -> str:
    "Single word"
    words = capture_to_words(m)
    return words[0]

@mod.capture(rule = "<user.capitalized_word> | <user.unmodified_word>")
def word(m) -> str:
    "Single word"
    return str(m)

@mod.capture(rule="(<user.word>)+")
def words(m) -> str:
    "Multiple words"
    return " ".join(capture_to_words(m))

@mod.capture(rule="(<user.word>)+")
def text(m) -> str:
    "text comprising multiple words"
    return " ".join(capture_to_words(m))

@mod.capture(rule="(<user.unmodified_word> | <user.number> | <phrase>)+")
def prose(m) -> str:
    """captures generic prose"""
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