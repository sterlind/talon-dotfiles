from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("expression_language")

mod.list("constants", "Simple language constants")
mod.list("known_functions", "Known function names")

mod.list("infix_other_operators", "Binary infix operators besides logical ones")
mod.list("infix_logical_operators", "Infix logical operators")
mod.list("unary_operators", "Unary prefix operators")

@mod.capture(rule="{user.infix_other_operators} | {user.infix_logical_operators} | {user.unary_operators}")
def operator_syntax(m) -> str:
    return str(m)

@mod.capture(rule="{user.infix_other_operators} | {user.infix_logical_operators}")
def infix_operator_syntax(m) -> str:
    return str(m)
    
@mod.capture(rule="{user.unary_operators} <user.value_syntax>")
def unary_logic_syntax(m) -> str:
    return actions.user.code_format_unary_operation(m.unary_operators, m.value_syntax)

@mod.capture(rule="<user.value_syntax> {user.infix_logical_operators} <user.value_syntax>")
def binary_logic_syntax(m) -> str:
    return actions.user.code_format_binary_operation(m.infix_logical_operators, m.value_syntax_1, m.value_syntax_2)

@mod.capture(rule="<user.unary_logic_syntax> | <user.binary_logic_syntax> | <user.value_syntax>")
def logic_syntax(m) -> str:
    return str(m)
    
@mod.capture(rule="<user.compound_name_syntax> ([and] <user.compound_name_syntax>)*")
def arguments_syntax(m) -> List[str]:
    return m.compound_name_syntax_list

@mod.capture(rule="string [<user.formatters_code>] <user.word_separated_string> [{user.keywords}]")
def string_constant_syntax(m) -> str:
    formatters = getattr(m, "formatters_code", None)
    text = m.word_separated_string
    if formatters:
        text = actions.user.insert_formatted(m.word_separated_string, formatters)
    return f"\"{text}\""

@mod.capture(rule="{user.constants} | <user.string_constant_syntax> | <user.compound_name_syntax> | <number>")
def value_syntax(m) -> str:
    return str(m)

@mod.capture(rule=" <user.compound_name_syntax> | {user.known_functions} ")
def called_function_syntax(m) -> str:
    function_name = getattr(m, "known_functions", None)
    if not function_name:
        function_name = actions.user.format_text(m.compound_name_syntax, settings.get("user.function_formatter"))
    return function_name

@mod.action_class
class UserActions:
    def code_format_unary_operation(operator: str, expression: str = None):
        """Formats a unary operation"""
    
    def code_format_binary_operation(operator: str, left: str = None, right: str = None):
        """Formats a binary operation"""
        
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        """Makes a list comprehension expression"""

    def code_expression_ternary(true_expression: str = None, false_expression: str = None, condition: str = None):
        """Makes a ternary expression"""

    def code_expression_lambda(parameters: List[str] = None):
        """Makes a lambda expression"""
    
    def code_expression_unary_operator(operator: str, expression: str = None):
        """Makes a unary operator"""

    def code_expression_binary_infix_operator(operator: str, left: str = None, right: str = None):
        """Makes a binary operator expression"""

    def code_expression_function_call(function_name: str):
        """Makes a function call expression"""

    def code_expression_index(index: str = None):
        """Appends an index to an expression"""