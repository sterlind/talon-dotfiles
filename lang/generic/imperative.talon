tag: user.imperative_language
-

# Control flow
if [call]: user.insert_snippet("if $1:\n\t$0")
if <user.logic_syntax>: user.insert_snippet("if {logic_syntax}:\n\t$0")

make for: user.insert_snippet("for $1 in $2:\n\t$0")
for <user.name_syntax> in:
    user.insert_snippet("for {name_syntax} in $1:\n\t$2")
for <user.name_syntax> in <user.name_syntax>:
    user.insert_snippet("for {name_syntax_1} in {name_syntax_2}:\n\t$1")

make while: user.insert_snippet("while $1:\n\t$0")
while <user.value_syntax>: insert("while {value_syntax}:\n\t")

make try: user.insert_snippet("try:\n\t$1\nexcept $2:\n\t$3")

with as <user.name_syntax>:
    user.insert_snippet("with $1 as {name_syntax}:\n\t$0")

make pass: insert("pass")

# Function declaration
funk <user.name_syntax>:
    user.insert_snippet("def {name_syntax}($1)$2:")
[which] takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list, ", ")