from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("expression_language")

mod.list("constants", "Simple language constants")

@mod.capture(rule="string [<user.formatters_code>] <user.word_separated_string> [{user.keywords}]")
def string_constant_syntax(m) -> str:
    formatters = getattr(m, "formatters_code", None)
    text = m.word_separated_string
    if formatters:
        text = actions.user.insert_formatted(m.word_separated_string, formatters)
    return f"\"{text}\""

@mod.capture(rule="{user.constants} | <user.string_constant_syntax> | <user.compound_name_syntax> | <number>")
def constant_syntax(m) -> str:
    return str(m)