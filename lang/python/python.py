from typing import List, Union
from talon import Module, Context, actions
from ..util import insert_placeholders 

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.python
"""

ctx.tags = [
    "user.generic_language",
    "user.class_language",
    "user.type_language",
    "user.expression_language",
    "user.statement_language",
    "user.imperative_language"
]

ctx.lists["self.primitive_type"] = {
    "string": "str",
    "int": "int",
    "bool": "bool",
    "boolean": "bool",
}

ctx.lists["self.complex_type"] = {
    "list": "List",
    "set": "set"
}

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

ctx.lists["self.infix_arithmetic_operators"] = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "divides": "/",
    "assign": "=",
    "pipe": "|",
    "amper": "&",
    "carrot": "^",
    "shift left": "<<",
    "shift right": ">>",
}

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
    "lore": "or",
    "land": "and",
    "or": "or",
    "and": "and",
    "in": "in"
}

ctx.lists["self.unary_logical_operators"] = {
    "not": "not"
}

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

ctx.lists["self.known_functions"] = {
    "string": "str",
    "int": "int",
    "length": "len",
    "is instance": "isinstance",
    "get adder": "getattr",
    "repper": "repr"
}

@ctx.action_class("user")
class UserActions:
    def format_parameter_syntax(name: str, type: str = None):
        if type:
            return f"{name}: {type}"
        else:
            return name

    def code_declare_import(module: str, named_imports: List[str]):
        names = ", ".join(named_imports)
        actions.user.insert_snippet(f"from {module} import {names}")
    
    # Generic syntax:
    def code_document(text: str):
        actions.user.insert_snippet(f"\"\"\"{text}\"\"\"")

    def code_comment(text: str):
        actions.user.insert_snippet(f"# {text}")
    
    # Expression syntax:
    def code_format_unary_operation(operator: str, expression: str = None):
        if expression:
            return f"{operator} {expression}"
        else:
            return operator
    
    def code_format_binary_operation(operator: str, left: str = None, right: str = None):
        return " ".join(filter(None, [left, operator, right]))
        
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        expression, key, iterator = insert_placeholders(expression, key, iterator)
        actions.user.insert_snippet(f"[{expression} for {key} in {iterator}]")

    def code_expression_ternary(true_expression: str = None, false_expression: str = None, condition: str = None):
        true_expression, condition, false_expression = insert_placeholders(true_expression, condition, false_expression)
        actions.user.insert_snippet(f"{true_expression} if {condition} else {false_expression}")
        
    def code_expression_lambda(parameters: List[str] = None):
        parameters = ", ".join(parameters) if parameters else "$1"
        actions.user.insert_snippet(f"lambda {parameters}: $0")

    def code_expression_unary_operator(operator: str, expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"{operator} {expression}")
        
    def code_expression_binary_infix_operator(operator: str, left: str = None, right: str = None):
        if not left:
            right = insert_placeholders(right)
            actions.user.insert_snippet(f"{operator} {right}")
        else:
            right = insert_placeholders(right)
            actions.user.insert_snippet(f"{left} {operator} {right}")

    def code_expression_function_call(function_name: str):
        actions.user.insert_snippet(f"{function_name}($1)")

    def code_expression_index(index: str = None):
        if index:
            actions.user.insert_snippet(f"[{index}]")
        else:
            actions.user.insert_snippet("[$0]")
        
    # Statement syntax:
    def code_declare_import(module: str, named_imports: list[str] = None):
        if named_imports:
            named_imports = ", ".join(named_imports)
            actions.user.insert_snippet(f"from {module} import {named_imports}")
        else:
            actions.user.insert_snippet(f"import {module}")

    def code_declare_function(name: str):
        actions.user.insert_snippet(f"def {name}($1)$2:")
    
    # Imperative syntax:
    def code_statement_variable_declare(name: Union[str, list[str]], value: str = None):
        actions.user.code_statement_variable_assign(name, value)

    def code_statement_variable_assign(name: Union[str, list[str]], value: str = None):
        value = insert_placeholders(value)
        if not isinstance(name, str):
            name = ", ".join(name)            
        actions.user.insert_snippet(f"{name} = {value}")

    def code_statement_return_nothing():
        actions.insert("return")

    def code_statement_return(expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"return {expression}")
        
    def code_block_if(expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"if {expression}:\n\t")
        
    def code_block_while(expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"while {expression}:\n\t")
        
    def code_block_for(name: str = None, expression: str = None):
        name, expression = insert_placeholders(name, expression)
        actions.user.insert_snippet(f"for {name} in {expression}:\n\t")

    def code_block_try_catch():
        actions.user.insert_snippet(f"try:\n\t$1\nexcept $2:\n\t$3\n")

    def code_block_scope(name: str, value: str = None):
        value = insert_placeholders(value)
        actions.user.insert_snippet(f"with {value} as {name}:")
    
    # Class syntax:
    def code_declare_class(name: str):
        actions.user.insert_snippet(f"class {name}:")
    
    def code_declare_constructor():
        actions.user.insert_snippet(f"def __init__(self$0):")