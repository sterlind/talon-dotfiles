from functools import reduce
from talon import Module, Context, actions, grammar
import re
from typing import List

mod = Module()
ctx = Context()

@mod.capture(rule="(<user.word>)+")
def words(m) -> str:
    "Multiple words"
    return " ".join(capture_to_words(m))

@mod.capture(rule="<user.formatted_string> | <user.words>")
def text(m) -> str:
    "Text comprising multiple words"
    return str(m)

@mod.capture(rule="(<user.unmodified_word> | <user.number> | {user.key_punctuation} | <phrase>)+")
def prose(m) -> str:
    """Captures generic prose"""
    return format_phrase(capture_to_words(m))

def format_phrase(words: List[str]) -> str:
    """Formats a phrase"""
    result = ""
    for k, w in enumerate(words):        
        if k > 0 and need_space_between(words[k-1], w):
            result += " "
        result += w
    return result

no_space_after = re.compile(r"""
    (?:
        [\s\-_/#@([{‘“]     # characters that never need space after them
    | (?<!\w)[$£€¥₩₽₹]    # currency symbols not preceded by a word character
    # quotes preceded by beginning of string, space, opening braces, dash, or other quotes
    | (?: ^ | [\s([{\-'"] ) ['"]
    )$""", re.VERBOSE)
no_space_before = re.compile(r"""
    ^(?:
        [\s\-_.,!?;:/%)\]}’”]   # characters that never need space before them
    | [$£€¥₩₽₹](?!\w)         # currency symbols not followed by a word character
    # quotes followed by end of string, space, closing braces, dash, other quotes, or some punctuation.
    | ['"] (?: $ | [\s)\]}\-'".,!?;:/] )
    )""", re.VERBOSE)

def capture_to_words(m):
    def parse(w):
        if isinstance(w, grammar.vm.Phrase):
            return actions.dictate.replace_words(actions.dictate.parse_words(w))
        return w.split(" ")
    return reduce(lambda x, y: x + y, map(parse, m))
    
def omit_space_before(text: str) -> bool:
    return not text or no_space_before.search(text)

def omit_space_after(text: str) -> bool:
    return not text or no_space_after.search(text)

def need_space_between(before: str, after: str) -> bool:
    return not (omit_space_after(before) or omit_space_before(after))