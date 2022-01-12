from typing import List
from talon import Module, Context, actions

mod = Module()
ctx = Context()
ctx.matches = r"""
tag: user.python
"""

mod.list("primitive_type", "known primitive types")
ctx.lists["self.primitive_type"] = {
    "string": "str",
    "int": "int",
    "bool": "bool",
    "boolean": "bool",
}

mod.list("complex_type", "known complex types")
ctx.lists["self.complex_type"] = {
    "List": "list",
    "set": "set"
}

mod.list("keywords", "grammar keywords")
ctx.lists["self.keywords"] = [
    "type",
    "arg",
    "funk",
    "and",
    "dot",
    "call",
    "takes",
    "also",
    "returns",
    "from",
    "map",
    "array",
    "try",
    "set",
    "class"
]

mod.list("infix_operators", "Binary infix operators")
ctx.lists["self.infix_operators"] = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "divides": "/",
    "less": "<",
    "more": ">",
    "less equal": "<=",
    "more equal": ">=",
    "equal": "==",
    "not equal": "!=",
    "or": "or",
    "and": "and"
}

mod.list("unary_operators", "Unary prefix operators")
ctx.lists["self.unary_operators"] = {
    "not": "not"
}

mod.list("constants", "Simple language constants")
ctx.lists["self.constants"] = {
    "true": "True",
    "false": "False",
    "none": "None",
    "empty string": "\"\""
}

@mod.capture(rule="{user.infix_operators} | {user.unary_operators}")
def operator_syntax(m) -> str:
    return str(m)

@mod.capture(rule="{user.complex_type} of {user.primitive_type}")
def complex_type_syntax(m) -> str:
    return f"{m.complex_type}[{m.primitive_type}]"

@mod.capture(rule="{user.primitive_type} | <user.complex_type_syntax>")
def type_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.letter_or_number> | (<user.word>+ [{user.keywords}])")
def name_syntax(m) -> str:
    try:
        return m.letter_or_number
    except AttributeError:
        return actions.user.format_text(" ".join(m.word_list), "SNAKE_CASE")

@mod.capture(rule="<user.name_syntax> [(dot <user.name_syntax>)+]")
def compound_name_syntax(m) -> str:
    return ".".join(m.name_syntax_list)

@mod.capture(rule="(<user.word>+ [{user.keywords}])")
def class_syntax(m) -> str:
    try:
        return m.letter_or_number
    except AttributeError:
        return actions.user.format_text(" ".join(m.word_list), "HAMMER_CASE")

@mod.capture(rule=" <user.name_syntax> [type <user.type_syntax>]")
def parameter_syntax(m) -> str:
    try:
        return f"{m.name_syntax}: {m.type_syntax}"
    except AttributeError:
        return m.name_syntax

@mod.capture(rule="<user.parameter_syntax> ([and] <user.parameter_syntax>)*")
def parameters_syntax(m) -> List[str]:
    return m.parameter_syntax_list



@mod.capture(rule="<user.compound_name_syntax> ([and] <user.compound_name_syntax>)*")
def arguments_syntax(m) -> List[str]:
    return m.compound_name_syntax_list

@mod.capture(rule="call <user.compound_name_syntax> [with <user.arguments_syntax>]")
def call_syntax(m) -> str:
    try:
        return f"{m.compound_name_syntax}({m.arguments_syntax})"
    except AttributeError:
        return f"{m.compound_name_syntax}()"

@mod.capture(rule="<user.formatted_string> | <user.number> | <user.compound_name_syntax> | {user.constants}")
def value_syntax(m) -> str:
    return str(m)

@mod.action_class
class UserActions:
    def code_import(module: str, named_imports: List[str]):
        "Inserts a from-import statement"
        names = ", ".join(named_imports)
        actions.user.insert_snippet(f"from {module} import {names}")
        
    def code_parameter(parameters: List[str], preamble: str = None):
        "Inserts one or more parameters into a function declaration"
        # print(repr(parameters))
        parameters = ", ".join(parameters)
        preamble = preamble or ""
        actions.user.insert_snippet(preamble + parameters)

    def code_function(name: str, args: List[str] = None):
        "inserts a function"
        # name = actions.user.format_text(name, "SNAKE_CASE")
        args = ", ".join(args) if args else ""
        actions.user.insert_snippet(f"def {name}({args}):\n\t$1")
