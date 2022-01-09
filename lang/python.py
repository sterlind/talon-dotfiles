from typing import List
from talon import Module, Context, actions

mod = Module()
ctx = Context()
ctx.matches = r"""
tag: user.python
"""

mod.list("known_types", "known types")
ctx.lists["self.known_types"] = {
    "string": "str",
    "int": "int"
}

mod.list("keywords", "grammar keywords")
ctx.lists["self.keywords"] = [
    "named",
    "type",
    "arg",
    "funk",
    "and",
    "dot"
]

@mod.capture(rule="<user.text> [{user.keywords}]")
def name_syntax(m) -> str:
    return actions.user.format_text(str(m.text), "SNAKE_CASE")

@mod.capture(rule=" <user.name_syntax> [type {user.known_types}]")
def parameter_syntax(m) -> str:
    try:
        return f"{m.name_syntax}: {m.known_types}"
    except AttributeError:
        return m.name_syntax

@mod.capture(rule="<user.parameter_syntax> ([and] <user.parameter_syntax>)*")
def parameters_syntax(m) -> List[str]:
    return m.parameter_syntax_list

@mod.capture(rule="<user.name_syntax> ([dot] <user.name_syntax>)*")
def compound_name_syntax(m) -> str:
    return ".".join(m.name_syntax_list)

@mod.capture(rule="<user.compound_name_syntax> ([and] <user.compound_name_syntax>)*")
def arguments_syntax(m) -> List[str]:
    return m.compound_name_syntax_list

@mod.action_class
class UserActions:
    # def code_argument(name: str, type: str = None):
    #     "inserts an argument"
    #     name = actions.user.format_text(name, "SNAKE_CASE")
    #     if type:
    #         actions.insert(f"{name}: {type}")
    #     else:
    #         actions.insert(f"{name}")
        
    def code_function(name: str, args: List[str] = None):
        "inserts a function"
        # name = actions.user.format_text(name, "SNAKE_CASE")
        args = ", ".join(args) if args else ""
        actions.user.insert_snippet(f"def {name}({args}):\n\t$1")
        