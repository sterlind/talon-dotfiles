tag: user.python
-

# Import statements
import <user.compound_name_syntax>: user.insert_snippet("import {compound_name_syntax}\n$0")
also import <user.value_syntax> (and <user.value_syntax>)*:
    user.code_parameter(value_syntax_list, ", ")
from <user.compound_name_syntax> import <user.name_syntax> ([and] <user.name_syntax>)*:
    user.code_import(compound_name_syntax, name_syntax_list)

# Comments
document <user.text>$:
    result = user.format_text(text, "SENTENCE_CASE")
    insert("\"\"\"{result}\"\"\"")
explain <user.text>$:
    result = user.format_text(text, "SENTENCE_CASE")
    insert("# {result}")

# [Expressions]
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
snip index: user.insert_snippet("[$1]$0")
index <user.value_syntax>: insert("[{value_syntax}]")

snip map: user.insert_snippet("{{\n\t$1\n}}")
snip array: user.insert_snippet("[\n\t$1\n]")

# Expression constructors
snip [list] comp: user.insert_snippet("[$1 for $2 in $3]")
list comp for <user.name_syntax> in: user.insert_snippet("[$2 for {name_syntax} in $1]")

lambda <user.name_syntax> [does]:
    insert("lambda {name_syntax}: ")

snip ternary: user.insert_snippet("$1 if $2 else $3")
<user.value_syntax> if <user.value_syntax> else <user.value_syntax>:
    insert("{value_syntax_1} if {value_syntax_2} else {value_syntax_3}")

# [Statements]
# Variable assignment
(set|var) <user.compound_name_syntax> (to|is): user.insert_snippet("{compound_name_syntax} = $1")
(set|var) <user.compound_name_syntax> (to|is) <user.value_syntax>: user.insert_snippet("{compound_name_syntax} = {value_syntax}")
var <user.compound_name_syntax>: insert(compound_name_syntax)

return nothing: user.insert_snippet("return")
return: user.insert_snippet("return $1")
return <user.value_syntax>: user.insert_snippet("return {value_syntax}$0")

# Control flow
if [call]: user.insert_snippet("if $1:\n\t$0")
if <user.value_syntax>: user.insert_snippet("if {value_syntax}:\n\t$0")
if not <user.value_syntax>: user.insert_snippet("if not {value_syntax}:\n\t$0")

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

# Top level syntax:
# Class declaration
declare class <user.class_syntax>: user.insert_snippet("class {class_syntax}:\n\t$0")

# Function declaration
funk <user.name_syntax>:
    user.insert_snippet("def {name_syntax}($1)$2:")
[which] takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list, ", ")
returns type <user.type_syntax>:
    user.vscode("jumpToNextSnippetPlaceholder")
    insert(" -> {type_syntax}")