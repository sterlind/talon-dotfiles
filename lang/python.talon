tag: user.python
-


funk <user.name_syntax>:
    user.insert_snippet("def {name_syntax}($1)$2:")
constructor:
    user.insert_snippet("def __init__($1)$2:")
[which] takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list, ", ")
pass <user.value_syntax> (and <user.value_syntax>)*:
    user.code_parameter(value_syntax_list)
also (pass|import) <user.value_syntax> (and <user.value_syntax>)*:
    user.code_parameter(value_syntax_list, ", ")
(document|dock) <phrase> [over]:
    user.insert_snippet("\"\"\"{phrase}\"\"\"")

returns type <user.type_syntax>:
    user.vscode("jumpToNextSnippetPlaceholder")
    insert(" -> {type_syntax}")
call <user.compound_name_syntax>: user.insert_snippet("{compound_name_syntax}($0)")
return <user.value_syntax>: user.insert_snippet("return {value_syntax}$0")
return: user.insert_snippet("return $1")
format: user.insert_snippet("f\"$0\"")
if: user.insert_snippet("if $1:\n\t$0")
if <user.value_syntax>: user.insert_snippet("if {value_syntax}:\n\t$0")
for <user.name_syntax> in:
    user.insert_snippet("for {name_syntax} in $1:\n\t$2")
comp: user.insert_snippet("[$1 for $2 in $3]")
comp for <user.name_syntax> in: user.insert_snippet("[$2 for {name_syntax} in $1]")
import <user.compound_name_syntax>: user.insert_snippet("import {compound_name_syntax}\n$0")
class <user.class_syntax>: user.insert_snippet("class {class_syntax}:\n\t$0")
from <user.compound_name_syntax> import <user.name_syntax> ([and] <user.name_syntax>)*:
    user.code_import(compound_name_syntax, name_syntax_list)
map: user.insert_snippet("{{\n\t$1\n\}}")
array: user.insert_snippet("[\n\t$1\n]")
lambda <user.name_syntax> [does]:
    user.insert_snippet("lambda {name_syntax}: $1")
set <user.compound_name_syntax> to: user.insert_snippet("{compound_name_syntax} = $1")
var <user.compound_name_syntax> is: user.insert_snippet("{compound_name_syntax} = $1")
var <user.compound_name_syntax>: insert(compound_name_syntax)
value <user.value_syntax>: insert(value_syntax)
try: user.insert_snippet("try:\n\t$1\nexcept $2:\n\t$3")
op <user.value_syntax> {user.infix_operators} <user.value_syntax>:
    user.insert_snippet("{value_syntax_1} {infix_operators} {value_syntax_2}$0")
op <user.operator_syntax>: insert(operator_syntax)
op <user.operator_syntax> <user.value_syntax>: user.insert_snippet(" {operator_syntax} {value_syntax}$0")
op <user.value_syntax> <user.operator_syntax>: user.insert_snippet("{value_syntax} {operator_syntax} $1")
index: user.insert_snippet("[$1]$0")
