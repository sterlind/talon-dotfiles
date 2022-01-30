tag: user.expression_language
-

# Generic
value <user.value_syntax>: insert(value_syntax)

# Function call
(call <user.called_function_syntax>)+: user.code_expression_function_call_list(called_function_syntax_list)
pass <user.value_syntax> (pass <user.value_syntax>)*:
    user.code_format_list(value_syntax_list)
also (pass|arg|args) <user.value_syntax> (pass <user.value_syntax>)*:
    user.code_format_list_append(value_syntax_list)

# Operations
# op <user.value_syntax> <user.infix_operator_syntax> <user.value_syntax>:
#     user.code_expression_binary_infix_operator(infix_operator_syntax, value_syntax_1, value_syntax_2)
# op <user.operator_syntax>: user.code_expression_binary_infix_operator(operator_syntax, "", "")
# op <user.operator_syntax> <user.value_syntax>: user.code_expression_binary_infix_operator(infix_operators, "", value_syntax)
# op <user.value_syntax> <user.operator_syntax>: user.code_expression_binary_infix_operator(infix_operators, value_syntax, "")
# op {user.unary_operators} <user.value_syntax>: user.code_expression_unary_operator(unary_operators, value_syntax)
# op <user.value_syntax> <user.infix_operator_syntax> <user.value_syntax>:
    # user.code_expression_binary_infix_operator(infix_operator_syntax, value_syntax_1, value_syntax_2)

# op <user.infix_operator_syntax> <user.value_syntax>:
    # user.code_expression_binary_infix_operator(infix_operator_syntax, "", value_syntax)

(condition|cond|bool) <user.condition_syntax>: insert("{condition_syntax}")
op <user.binary_logic_syntax_tail>: insert(" {binary_logic_syntax_tail}")
op <user.binary_arithmetic_syntax_tail>: insert(" {binary_arithmetic_syntax_tail}")

# Constants
condition <user.value_syntax>: insert("{value_syntax}")
make {user.constants}: insert("{constants}")
index [<user.value_syntax>]: user.code_expression_index(value_syntax or "")

# Expression constructors
make [list] comp: user.code_expression_list_comprehension()
list comp for <user.name_syntax> in: user.code_expression_list_comprehension("", name_syntax)

lambda <user.name_syntax> ([and] <user.name_syntax>)* [does]: user.code_expression_lambda(name_syntax_list)

make ternary: user.code_expression_ternary()
<user.value_syntax> if <user.value_syntax> else <user.value_syntax>:
    user.code_expression_ternary(value_syntax_1, value_syntax_3, value_syntax_2)