from typing import List, Union
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

ctx.lists["self.infix_arithmetic_operators"] = {
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
    "or": "||",
    "and": "&&",
    "in": "in"
}

ctx.lists["self.unary_operators"] = {
    "not": "!"
}

ctx.lists["self.constants"] = {
    "true": "true",
    "false": "false",
    "none": "null",
    "null": "null",
    "empty string": "\"\"",
    "empty array": "[]",
    "empty list": "[]",
    "empty dictionary": "{}",
    "empty dict": "{}",
    "empty map": "{}",
}

ctx.lists["self.known_functions"] = {
}

BLOCK_PATTERN = "{$0\n}"

@ctx.action_class("user")
class UserActions:
    def format_parameter_syntax(name: str, type: str = None):
        if type:
            return f"{name}: {type}"
        else:
            return name

    # Generic syntax:
    def code_document(text: str):        
        actions.user.insert_snippet(f"/**\n * {text}$1\n */\n$0")

    def code_comment(text: str):
        actions.user.insert_snippet(f"// {text}")
    
    # Expression syntax:
    def code_format_unary_operation(operator: str, expression: str = None):
        return f"{operator}{expression}"
    
    def code_format_binary_operation(operator: str, left: str = None, right: str = None):
        return f"{left} {operator} {right}"
        
    def code_expression_list_comprehension(expression: str = None, key: str = None, iterator: str = None):
        pass

    def code_expression_ternary(true_expression: str = None, false_expression: str = None, condition: str = None):
        condition, true_expression, false_expression = insert_placeholders(condition, true_expression, false_expression)
        actions.user.insert_snippet(f"{condition} ? {true_expression} : {false_expression}")        
        
    def code_expression_lambda(parameters: List[str] = None):
        parameters_string = None
        if parameters:
            if len(parameters) > 1:
                parameters_string = ", ".join(parameters)
                parameters_string = f"({parameters_string})"
            else:
                parameters_string = parameters[0]
        else:
            parameters_string = "$1"
                
        actions.user.insert_snippet(f"{parameters_string} => $0")

    def code_expression_unary_operator(operator: str, expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"{operator} {expression}")
        pass
        
    def code_expression_binary_infix_operator(operator: str, left: str = None, right: str = None):
        left, right = insert_placeholders(left, right)
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
            names = ", ".join(named_imports)
            actions.user.insert_snippet(f"import {names} from \"{module}\";")
        else:
            actions.user.insert_snippet(f"import * from \"{module}\";")

    def code_declare_function(name: str):
        actions.user.insert_snippet(f"function {name}($1)$2 {BLOCK_PATTERN}")
    
    # Imperative syntax:
    def code_statement_variable_declare(name: Union[str, list[str]], type: str = None, value: str = None):
        value = insert_placeholders(value)
        actions.user.insert_snippet(f"{type} {name} = {value};")

    def code_statement_variable_assign(name: Union[str, list[str]], value: str = None):
        value = insert_placeholders(value)
        actions.user.insert_snippet(f"{name} = {value};")

    def code_statement_return_nothing():
        actions.insert("return;")

    def code_statement_return(expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"return {expression};")
        
    def code_block_if(expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"if ({expression}) {BLOCK_PATTERN}")
        
    def code_block_while(expression: str = None):
        expression = insert_placeholders(expression)
        actions.user.insert_snippet(f"while ({expression}) {BLOCK_PATTERN}")
        
    def code_block_for(name: str = None, expression: str = None):
        name, expression = insert_placeholders(name, expression)
        actions.user.insert_snippet(f"for (const {name} of {expression}) {BLOCK_PATTERN}")

    def code_block_try_catch():
        actions.user.insert_snippet(f"try {{\n\t$1\n}} catch ($2) {BLOCK_PATTERN}")

    def code_block_scope(name: str, value: str = None):
        pass
    
    # Class syntax:
    def code_declare_class(name: str):
        pass
    
    def code_declare_constructor():
        pass