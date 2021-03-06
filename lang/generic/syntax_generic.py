from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("generic_language")

mod.setting("constant_formatter", str)
mod.setting("variable_formatter", str)

mod.list("keywords", "grammar keywords")
mod.list("symbols", "Symbols currently in scope")

@mod.capture(rule="<user.word>+ [{user.keywords}]")
def raw_name_syntax(m) -> List[str]:
    return m.word_list

@mod.capture(rule="(const|constant) <user.raw_name_syntax>")
def constant_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.constant_formatter"))

@mod.capture(rule="<user.raw_name_syntax>")
def variable_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.variable_formatter"))

@mod.capture(rule="{user.symbols} | <user.letter> | <user.constant_name_syntax> | <user.variable_name_syntax>")
def name_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.name_syntax> [(dot <user.name_syntax>)+]")
def compound_name_syntax(m) -> str:
    return ".".join(m.name_syntax_list)

@mod.action_class
class UserActions:
    def code_format_list(elements: list[str]) -> str:
        """Formats a list of elements"""
        actions.user.insert_snippet(", ".join(elements))

    def code_format_list_append(elements: list[str]):
        """Formats an appended list of elements"""
        parameters = ", ".join(elements)
        actions.user.insert_snippet(", " + parameters)
        
    def code_document(text: str):
        """Formal documentation"""

    def code_comment(text: str):
        """Inserts a comment"""