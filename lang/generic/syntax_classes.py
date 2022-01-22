from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("class_language")

@mod.capture(rule="<user.raw_name_syntax>")
def class_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.class_formatter"))