from talon import Module, Context, actions
import re
from typing import List, Union

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

@mod.capture(rule="{self.formatter_code}+")
def formatters_code(m) -> str:
    "Returns comma-separated formatter list."
    return ",".join(m.formatter_code_list)

@mod.capture(rule="<user.formatters_code>")
def formatters(m) -> str:
    """Shim for formatters_code"""
    return str(m)

@mod.action_class
class Actions:
    def format_text(text: Union[str, List[str]], formatters: str) -> str:
        "Formats text with comma-separated formatter list."
        if not isinstance(text, str):
            text = " ".join(text)
        for format in reversed(formatters.split(",")):
            text = formatters_list[format](text)
        return text

    def unformat_text(text: str) -> str:
        """Remove format from text"""
        # Remove quotes
        text = de_string(text)
        # Split on delimiters. A delimiter char followed by a blank space is no delimiter.
        result = re.sub(r"[-_.:/](?!\s)+", " ", text)
        # Split camel case. Including numbers
        result = de_camel(result)
        # Delimiter/camel case successfully split. Lower case to restore "original" text.
        if text != result:
            result = result.lower()
        return result    

def format_words(text, splitter, delimiter, func_first=None, func_rest=None):
    func_first = func_first or none
    func_rest = func_rest or none
    words = splitter(text)
    transform = [func_first(words[0])] + [func_rest(w) for w in words[1:]]
    return delimiter.join(transform)

def de_camel(text: str) -> str:
    """Replacing camelCase boundaries with blank space"""
    return re.sub(
        r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])",
        " ",
        text,
    )

def de_string(text: str) -> str:
    """Remove quotes around a selected string"""
    if text[0] == "'" or text[0] == '"':
        text = text[1:]
    if text[-1] == "'" or text[-1] == '"':
        text = text[:-1]
    return text
    
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