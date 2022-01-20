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
    "list": "List",
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
    "state",
    "op",
    "index"
    # "class"
]

mod.list("infix_other_operators", "Binary infix operators besides logical ones")
ctx.lists["self.infix_other_operators"] = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "divides": "/",
    "assign": "="
}

mod.list("infix_logical_operators", "Infix logical operators")
ctx.lists["self.infix_logical_operators"] = {
    "less": "<",
    "less than": "<",
    "more": ">",
    "greater than": ">",
    "less equal": "<=",
    "is greater or equal to": ">=",
    "greater equals": ">=",
    "equal": "==",
    "is not": "!=",
    "is not equal to": "!=",
    "not equals": "!=",
    "or": "or",
    "and": "and",
    "in": "in"
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
    "empty string": "\"\"",
    "empty array": "[]",
    "empty list": "[]",
    "empty dictionary": "{}",
    "empty dict": "{}",
    "empty map": "{}",
}

mod.list("known_functions", "Known function names")
ctx.lists["self.known_functions"] = {
    "string": "str",
    "int": "int",
    "length": "len",
    "is instance": "isinstance",
    "get adder": "getattr"
}

@mod.capture(rule="{user.infix_other_operators} | {user.infix_logical_operators} | {user.unary_operators}")
def operator_syntax(m) -> str:
    return str(m)

@mod.capture(rule="{user.complex_type} of {user.primitive_type}")
def complex_type_syntax(m) -> str:
    return f"{m.complex_type}[{m.primitive_type}]"

@mod.capture(rule="{user.primitive_type} | <user.complex_type_syntax>")
def type_syntax(m) -> str:
    return str(m)

# @mod.capture(rule="nothing | <user.letter> | (<user.word>+ [{user.keywords}])")
@mod.capture(rule="<user.word>+ [{user.keywords}]")
def raw_name_syntax(m) -> List[str]:
    return m.word_list

@mod.capture(rule="const <user.raw_name_syntax>")
def constant_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, "ALL_CAPS,SNAKE_CASE")

@mod.capture(rule="<user.raw_name_syntax>")
def variable_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, "SNAKE_CASE")
    
@mod.capture(rule="<user.letter> | <user.constant_name_syntax> | <user.variable_name_syntax>")
def name_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.raw_name_syntax>")
def class_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, "HAMMER_CASE")

@mod.capture(rule="<user.name_syntax> [(dot <user.name_syntax>)+]")
def compound_name_syntax(m) -> str:
    return ".".join(m.name_syntax_list)

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

@mod.capture(rule = "{user.known_functions} | <user.compound_name_syntax>")
def function_name_syntax(m) -> str:
    return str(m)

@mod.capture(rule="call <user.function_name_syntax> [with <user.arguments_syntax>]")
def call_syntax(m) -> str:
    try:
        return f"{m.function_name_syntax}({m.arguments_syntax})"
    except AttributeError:
        return f"{m.function_name_syntax}()"

@mod.capture(rule="{user.unary_operators} <user.value_syntax>")
def unary_logic_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.value_syntax> {user.infix_logical_operators} <user.value_syntax>")
def binary_logic_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.unary_logic_syntax> | <user.binary_logic_syntax> | <user.value_syntax>")
def logic_syntax(m) -> str:
    return str(m)

@mod.capture(rule="string [<user.formatters_code>] <user.word_separated_string> [{user.keywords}]")
def string_constant_syntax(m) -> str:
    formatters = getattr(m, "formatters_code", None)
    text = m.word_separated_string
    if formatters:
        text = actions.user.insert_formatted(m.word_separated_string, formatters)
    return f"\"{text}\""

@mod.capture(rule=" {user.constants} | <user.string_constant_syntax> | <user.compound_name_syntax> | <number>")
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
