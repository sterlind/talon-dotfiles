tag: user.statement_language
-

# Import statements
import <user.compound_name_syntax>: user.code_declare_import(compound_name_syntax)
also import <user.name_syntax> (and <user.name_syntax>)*:
    user.code_format_list_append(name_syntax_list)
from <user.compound_name_syntax> import <user.name_syntax> ([and] <user.name_syntax>)*:
    user.code_declare_import(compound_name_syntax, name_syntax_list)

# Function declaration
funk <user.name_syntax>:
    user.code_declare_import(name_syntax)
[which] takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_format_list_append(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_format_list_append(parameter_syntax_list)