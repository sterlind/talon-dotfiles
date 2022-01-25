from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("expression_language")

mod.list("infix_arithmetic_operators", "Binary infix operators besides logical ones")
mod.list("infix_logical_operators", "Infix logical operators")
mod.list("unary_arithmetic_operators", "Unary prefix operators")
mod.list("unary_logical_operators", "Unary prefix operators")

@mod.capture(rule="<user.compound_name_syntax> | <user.constant_syntax>")
def value_syntax_l1(m) -> str:
    # L1 captures primitive values, such as constants and names.
    return str(m)

@mod.capture(rule="{user.unary_logical_operators} <user.value_syntax_l2>")
def unary_logic_syntax(m) -> str:
    return actions.user.code_format_unary_operation(m.unary_logical_operators, m.value_syntax_l2)

@mod.capture(rule="{user.infix_logical_operators} <user.value_syntax_l2>")
def binary_logic_syntax_tail(m) -> str:
    return actions.user.code_format_binary_operation("", m.infix_logical_operators, m.value_syntax_l2)

@mod.capture(rule="<user.value_syntax_l2> (<user.binary_logic_syntax_tail>)+")
def binary_logic_syntax(m) -> str:
    tail = " ".join(m.binary_logic_syntax_tail_list)
    return f"{m.value_syntax_l2} {tail}"

@mod.capture(rule="<user.value_syntax_l2> | <user.unary_logic_syntax> | <user.binary_logic_syntax>")
def condition_syntax(m) -> str:
    # This may be a boolean or any other kind of constant, such as a string.
    # Might want to restrict this further, but we need to keep everything in the tail.
    return str(m)

@mod.capture(rule="(condition|cond|bool) <user.condition_syntax>")
def explicit_condition_syntax(m) -> str:
    # Logical "and" is ambiguous with "and" used as a keyword delimiting lists and arguments.
    # This allows you to explicitly toggle to condition mode, as if you were inside an if-statement.
    return m.condition_syntax

@mod.capture(rule="{user.unary_arithmetic_operators} <user.value_syntax_l1>")
def unary_arithmetic_syntax(m) -> str:
    return actions.user.code_format_unary_operation(m.unary_arithmetic_operators, m.value_syntax_l1)

@mod.capture(rule="{user.infix_arithmetic_operators} <user.value_syntax_l1>")
def binary_arithmetic_syntax_tail(m) -> str:
    return actions.user.code_format_binary_operation("", m.infix_arithmetic_operators, m.value_syntax_l1)

@mod.capture(rule="<user.value_syntax_l1> (<user.binary_arithmetic_syntax_tail>)+")
def binary_arithmetic_syntax(m) -> str:
    tail = " ".join(m.binary_arithmetic_syntax_tail_list)
    return f"{m.value_syntax_l1} {tail}"

@mod.capture(rule="<user.value_syntax_l1> | <user.unary_arithmetic_syntax> | <user.binary_arithmetic_syntax>")
def value_syntax_l2(m) -> str:
    # L2 captures L1 as well as expressions of non-logical operators (e.g. +)
    return str(m)

@mod.capture(rule="<user.explicit_condition_syntax> | <user.value_syntax_l2>")
def value_syntax(m) -> str:
    # This is the default capture for values outside of condition statements.
    # Expressions of logical operators can be brought in explicitly.
    return str(m)

@mod.capture(rule="<user.value_syntax> | <user.condition_syntax>")
def value_or_condition_syntax(m) -> str:
    return str(m)

@mod.action_class
class UserActions:
    def code_format_unary_operation(operator: str, expression: str = None):
        """Formats a unary operation"""
    
    def code_format_binary_operation(operator: str, left: str = None, right: str = None):
        """Formats a binary operation"""
        
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        """Makes a list comprehension expression"""

    def code_expression_unary_operator(operator: str, expression: str = None):
        """Makes a unary operator"""

    def code_expression_binary_infix_operator(operator: str, left: str = None, right: str = None):
        """Makes a binary operator expression"""