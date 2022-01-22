from talon import Context, Module, actions
from typing import List

mod = Module()
mod.tag("language_expressions")

mod.list("infix_other_operators", "Binary infix operators besides logical ones")
mod.list("infix_logical_operators", "Infix logical operators")
mod.list("unary_operators", "Unary prefix operators")

@mod.capture(rule="{user.infix_other_operators} | {user.infix_logical_operators} | {user.unary_operators}")
def operator_syntax(m) -> str:
    return str(m)
    
@mod.capture(rule="{user.unary_operators} <user.value_syntax>")
def unary_logic_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.value_syntax> {user.infix_logical_operators} <user.value_syntax>")
def binary_logic_syntax(m) -> str:
    return str(m)

@mod.capture(rule="<user.unary_logic_syntax> | <user.binary_logic_syntax> | <user.value_syntax>")
def logic_syntax(m) -> str:
    return str(m)
    
@mod.action_class
class UserActions:
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        """Makes a list comprehension expression"""

    def code_expression_ternary(true_expression: str = None, false_expression: str = None, condition: str = None):
        """Makes a ternary expression"""

    def code_expression_lambda(parameters: List[str] = None):
        """Makes a lambda expression"""