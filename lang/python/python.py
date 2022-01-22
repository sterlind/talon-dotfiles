from typing import List
from talon import Module, Context, actions

mod = Module()
ctx = Context()
ctx.matches = r"""
tag: user.python
"""
ctx.tags = ["user.generic_language", "user.class_language", "user.type_language"]

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
    "string": "str",
    "int": "int",
    "length": "len",
    "is instance": "isinstance",
    "get adder": "getattr"
}

@ctx.action_class("user")
class UserActions:
    def format_parameter_syntax(name: str, type: str = None):
        if type:
            return f"{name}: {type}"
        else:
            return name

    def code_import(module: str, named_imports: List[str]):
        names = ", ".join(named_imports)
        actions.user.insert_snippet(f"from {module} import {names}")
        
    def code_parameter(parameters: List[str], preamble: str = None):
        parameters = ", ".join(parameters)
        preamble = preamble or ""
        actions.user.insert_snippet(preamble + parameters)

    def code_function(name: str, args: List[str] = None):
        args = ", ".join(args) if args else ""
        actions.user.insert_snippet(f"def {name}({args}):\n\t$1")
    