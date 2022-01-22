tag: user.statement_language
-

# Import statements
import <user.compound_name_syntax>: user.insert_snippet("import {compound_name_syntax}\n$0")
also import <user.value_syntax> (and <user.value_syntax>)*:
    user.code_parameter(value_syntax_list, ", ")
from <user.compound_name_syntax> import <user.name_syntax> ([and] <user.name_syntax>)*:
    user.code_import(compound_name_syntax, name_syntax_list)

# Function declaration
funk <user.name_syntax>:
    user.insert_snippet("def {name_syntax}($1)$2:")
[which] takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list, ", ")