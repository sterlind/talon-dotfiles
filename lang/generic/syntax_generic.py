from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("generic_language")

mod.list("keywords", "grammar keywords")
mod.list("infix_other_operators", "Binary infix operators besides logical ones")
mod.list("infix_logical_operators", "Infix logical operators")
mod.list("unary_operators", "Unary prefix operators")
mod.list("constants", "Simple language constants")
mod.list("known_functions", "Known function names")

@mod.capture(rule="{user.infix_other_operators} | {user.infix_logical_operators} | {user.unary_operators}")
def operator_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.word>+ [{user.keywords}]")
def raw_name_syntax(m) -> List[str]:
    return m.word_list

@mod.capture(rule="const <user.raw_name_syntax>")
def constant_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.constant_formatter"))

@mod.capture(rule="<user.raw_name_syntax>")
def variable_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.variable_formatter"))

@mod.capture(rule="<user.letter> | <user.constant_name_syntax> | <user.variable_name_syntax>")
def name_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.name_syntax> [(dot <user.name_syntax>)+]")
def compound_name_syntax(m) -> str:
    return ".".join(m.name_syntax_list)

@mod.capture(rule="<user.name_syntax>")
def parameter_syntax(m) -> str:
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
    def format_parameter_syntax(name: str, type: str):
        "Formats a parameter with a type"

    def code_import(module: str, named_imports: List[str] = None):
        "Inserts a from-import statement"
        
    def code_parameter(parameters: List[str], preamble: str = None):
        "Inserts one or more parameters into a function declaration"

    def code_function(name: str, args: List[str] = None):
        "inserts a function"