tag: user.imperative_language
-
tag(): user.expression_language

# Variable assignment
(set var|declare) <user.compound_name_syntax> (and <user.compound_name_syntax>)+ (to|is):
    user.code_statement_variable_declare(compound_name_syntax_list)
(set var|declare) <user.compound_name_syntax> (and <user.compound_name_syntax>)+ (to|is) <user.value_syntax>:
    user.code_statement_variable_declare(compound_name_syntax_list, value_syntax)

(set var|declare) <user.compound_name_syntax> (to|is):
    user.code_statement_variable_declare(compound_name_syntax)
(set var|declare) <user.compound_name_syntax> (to|is) <user.value_syntax>:
    user.code_statement_variable_declare(compound_name_syntax, value_syntax)

set <user.compound_name_syntax> (and <user.compound_name_syntax>)+ (to|is):
    user.code_statement_variable_assign(compound_name_syntax_list)
set <user.compound_name_syntax> (and <user.compound_name_syntax>)+ (to|is) <user.value_syntax>:
    user.code_statement_variable_assign(compound_name_syntax_list, value_syntax)

set <user.compound_name_syntax> (to|is):
    user.code_statement_variable_assign(compound_name_syntax)
set <user.compound_name_syntax> (to|is) <user.value_syntax>:
    user.code_statement_variable_assign(compound_name_syntax, value_syntax)

return nothing: user.code_statement_return_nothing()
return: user.code_statement_return()
return <user.value_syntax>: user.code_statement_return(value_syntax)

if [call]: user.code_block_if()
if <user.condition_syntax>: user.code_block_if(condition_syntax)

make for: user.code_block_for()
for <user.name_syntax> in: user.code_block_for(name_syntax)
for <user.name_syntax> in <user.value_syntax>: user.code_block_for(name_syntax, value_syntax)

make while: user.code_block_while()
while <user.condition_syntax>: user.code_block_while(condition_syntax)

make try: user.code_block_try_catch()

with as <user.name_syntax>: user.code_block_scope(name_syntax)