from talon import Module, actions, settings
from typing import List

mod = Module()
mod.tag("expression_language")

mod.list("known_functions", "Known function names")

@mod.capture(rule="<user.compound_name_syntax> (and <user.compound_name_syntax>)*")
def arguments_syntax(m) -> List[str]:
    return m.compound_name_syntax_list

@mod.capture(rule="<user.compound_name_syntax> | {user.known_functions}")
def called_function_syntax(m) -> str:
    function_name = getattr(m, "known_functions", None)
    if not function_name:
        function_name = actions.user.format_text(m.compound_name_syntax, settings.get("user.function_formatter"))
    return function_name

@mod.action_class
class UserActions:
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        """Makes a list comprehension expression"""

    def code_expression_ternary(true_expression: str = None, false_expression: str = None, condition: str = None):
        """Makes a ternary expression"""

    def code_expression_lambda(parameters: List[str] = None):
        """Makes a lambda expression"""
    
    def code_expression_function_call(function_name: str):
        """Makes a function call expression"""

    def code_expression_function_call_list(function_names: list[str]):
        """Makes a chain of function call expression"""
        # We have to do this because otherwise "call" gets incorporated into the function name.
        # If precedence is changed, then we can drop this
        for name in function_names:
            actions.user.code_expression_function_call(name)

    def code_expression_index(index: str = None):
        """Appends an index to an expression"""