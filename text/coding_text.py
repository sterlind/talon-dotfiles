from talon import Module, actions
from itertools import tee
from typing import List

mod = Module()

@mod.capture(rule = "(<user.word> | {user.key_symbol})+")
def word_separated_string(m) -> str:
    "Returns a word separated string"
    def both_words(left, right) -> bool:
        return left.isalnum() and right.isalnum()
    return smart_spacing(list(m), space_between(both_words), " ")    
    
@mod.capture(rule="(<user.formatters_code> <user.word_separated_string> [over])")
def formatted_string(m) -> str:
    "Returns a formatted string"
    return actions.user.format_text(m.word_separated_string, m.formatters_code)

# FIXME: Talon is still on Python 3.9, pairwise is 3.10+
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
    
def space_between(needs_space):
    return lambda left, right: needs_space(left, right) if left and right else False

def smart_spacing(words: List[str], needs_space, separator: str) -> str:
    def emit(left, right):
        if needs_space(left, right):
            return [separator, right] if right else [separator]
        return [right] if right else []
    tokens = [emit(x[0], x[1]) for x in pairwise([None] + words + [None])]
    return "".join([item for sublist in tokens for item in sublist])