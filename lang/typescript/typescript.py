from typing import List
from talon import Module, Context, actions
from ..util import insert_placeholders

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.typescript
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

ctx.lists["self.complex_type"] = {}

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

ctx.lists["self.infix_other_operators"] = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "divides": "/",
    "assign": "="
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
    "or": "or",
    "and": "and",
    "in": "in"
}

ctx.lists["self.unary_operators"] = {
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
}

@ctx.action_class("user")
class UserActions:
    def format_parameter_syntax(name: str, type: str = None):
        return f"{name}: {type}"

    def code_declare_import(module: str, named_imports: List[str]):
        names = ", ".join(named_imports)
        actions.user.insert_snippet(f"import {names} from \"{module}\";")
    
    # Generic syntax:
    def code_document(text: str):        
        actions.user.insert_snippet(f"/**\n * {text}$1\n */\n$0")

    def code_comment(text: str):
        actions.user.insert_snippet(f"// {text}")
    
    # Expression syntax:
    def code_format_unary_operation(operator: str, expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"{operator} {expression}")
    
    def code_format_binary_operation(operator: str, left: str = None, right: str = None):
        actions.user.insert_snippet(f"{left} {operator} {right}")
        
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        pass

    def code_expression_ternary(true_expression: str = None, false_expression: str = None, condition: str = None):
        actions.user.insert_snippet(f"{condition} ? {true_expression} : {false_expression}")
        
        
    def code_expression_lambda(parameters: List[str] = None):
        pass
        pass

    def code_expression_unary_operator(operator: str, expression: str = None):
        pass
        pass
        
    def code_expression_binary_infix_operator(operator: str, left: str = None, right: str = None):
        pass
        pass

    def code_expression_function_call(function_name: str):
        pass

    def code_expression_index(index: str = None):
        pass
        
    # Statement syntax:
    def code_declare_import(module: str, named_imports: list[str] = None):
        pass

    def code_declare_function(name: str):
        pass
    
    # Imperative syntax:
    def code_statement_variable_assign(name: str, value: str = None):
        pass
        pass

    def code_statement_return_nothing():
        pass

    def code_statement_return(expression: str = None):
        pass
        pass
        
    def code_block_if(expression: str = None):
        pass
        pass
        
    def code_block_while(expression: str = None):
        pass
        pass
        
    def code_block_for(name: str = None, expression: str = None):
        pass
        pass

    def code_block_try_catch():
        pass

    def code_block_scope(name: str, value: str = None):
        pass
        pass
    
    # Class syntax:
    def code_declare_class(name: str):
        pass
    
    def code_declare_constructor():
        pass