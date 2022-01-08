from typing import List
from talon import Module, Context

mod = Module()
ctx = Context()

formatters_list = {
    "NOOP": lambda text: text,
    "ALL_CAPS": lambda text: text.upper(),
    "PROPER_CASE": lambda text: format_words(text, split, "", capitalize, lower),
    "DOUBLE_QUOTED_STRING": lambda text: f"\"{text}\"",
    "SNAKE_CASE": lambda text: format_words(text, split, "_", lower, lower),
    "HAMMER_CASE": lambda text: format_words(text, split, "", capitalize, capitalize),
    "CAMEL_CASE": lambda text: format_words(text, split, "", lower, capitalize)
}

mod.list("formatter_code", desc="Code formatters")
ctx.lists["self.formatter_code"] = {
    "proper": "PROPER_CASE",
    "upper": "ALL_CAPS",
    "string": "DOUBLE_QUOTED_STRING",
    "snake": "SNAKE_CASE",
    "hammer": "HAMMER_CASE",
    "camel": "CAMEL_CASE"
}

@mod.capture(rule="{self.formatter_code}+")
def formatters_code(m) -> str:
    "Returns comma-separated formatter list."
    return ",".join(m.formatter_code_list)

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