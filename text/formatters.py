from talon import Module, Context, actions
from itertools import tee
from typing import List

mod = Module()
ctx = Context()

formatters_list = {
    "NOOP": lambda text: text,
    "ALL_CAPS": lambda text: text.upper(),
    "PROPER_CASE": lambda text: format_words(text, split, "", capitalize, lower),
    "SENTENCE_CASE": lambda text: format_words(text, split, " ", capitalize, lower),
    "DOUBLE_QUOTED_STRING": lambda text: f"\"{text}\"",
    "SNAKE_CASE": lambda text: format_words(text, split, "_"),
    "HAMMER_CASE": lambda text: format_words(text, split, "", capitalize, capitalize),
    "CAMEL_CASE": lambda text: format_words(text, split, "", lower, capitalize),
    "KEBAB_CASE": lambda text: format_words(text, split, "-"),
    "SMASH_CASE": lambda text: format_words(text, split, "")
}

mod.list("formatter_code", desc="Code formatters")
ctx.lists["self.formatter_code"] = {
    "say": "SENTENCE_CASE",
    "proper": "PROPER_CASE",
    "upper": "ALL_CAPS",
    "string": "DOUBLE_QUOTED_STRING",
    "snake": "SNAKE_CASE",
    "hammer": "HAMMER_CASE",
    "camel": "CAMEL_CASE",
    "kabab": "KEBAB_CASE",
    "smash": "SMASH_CASE"
}

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

@mod.capture(rule="{self.formatter_code}+")
def formatters_code(m) -> str:
    "Returns comma-separated formatter list."
    return ",".join(m.formatter_code_list)

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

@mod.action_class
class Actions:
    def format_text(text: str, formatters: str) -> str:
        "Formats text with comma-separated formatter list."
        for format in reversed(formatters.split(",")):
            text = formatters_list[format](text)
        return text

def format_words(text, splitter, delimiter, func_first=None, func_rest=None):
    func_first = func_first or none
    func_rest = func_rest or none
    words = splitter(text)
    transform = [func_first(words[0])] + [func_rest(w) for w in words[1:]]
    return delimiter.join(transform)

def split(text: str) -> List[str]:
    return text.split(" ")

def upper(text: str) -> str:
    return text.upper()

def lower(text: str) -> str:
    return text.lower()

def capitalize(text: str) -> str:
    return text.capitalize()

def none(text: str) -> str:
    return text