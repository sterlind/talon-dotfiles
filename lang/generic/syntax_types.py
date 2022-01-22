from talon import Module, Context, actions, settings
from typing import List

mod = Module()
mod.tag("type_language")

mod.list("primitive_type", "known primitive types")
mod.list("complex_type", "known complex types")

ctx = Context()
ctx.matches = r"tag: user.type_language"
ctx.tags = ["user.generic_language"]

@mod.capture(rule="{user.complex_type} of {user.primitive_type}")
def complex_type_syntax(m) -> str:
    return f"{m.complex_type}[{m.primitive_type}]"
    
@mod.capture(rule="{user.primitive_type} | <user.complex_type_syntax>")
def type_syntax(m) -> str:
    return str(m)

@ctx.capture("user.parameter_syntax", rule="<user.name_syntax> [type <user.type_syntax>]")
def parameter_syntax(m) -> str:
    return actions.user.format_parameter_syntax(m.name_syntax, getattr(m, "type_syntax", None))

@mod.action_class
class UserActions:
    def format_parameter_syntax(name: str, type: str = None):
        "Formats a parameter with a type"