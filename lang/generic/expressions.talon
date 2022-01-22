tag: user.language_expressions
-

# Generic
value <user.value_syntax>: insert(value_syntax)

# Function call
call <user.function_name_syntax>: user.insert_snippet("{function_name_syntax}($0)")
constructor:
    user.insert_snippet("def __init__($1)$2:")
pass <user.value_syntax> (and <user.value_syntax>)*:
    user.code_parameter(value_syntax_list)
also (pass|arg|args) <user.value_syntax> (and <user.value_syntax>)*:
    user.code_parameter(value_syntax_list, ", ")

# Operations
op <user.value_syntax> {user.infix_operators} <user.value_syntax>:
    insert("{value_syntax_1} {infix_operators} {value_syntax_2}")
op <user.operator_syntax>: insert(" {operator_syntax} ")
op <user.operator_syntax> <user.value_syntax>: insert(" {operator_syntax} {value_syntax}")
op <user.value_syntax> <user.operator_syntax>: insert("{value_syntax} {operator_syntax} ")

# Constants
make {user.constants}: insert("{constants}")
make index: user.insert_snippet("[$1]$0")
index <user.value_syntax>: insert("[{value_syntax}]")