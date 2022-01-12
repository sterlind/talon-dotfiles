tag: user.python
-


funk <user.name_syntax>:
    user.insert_snippet("def {name_syntax}($1)$2:")
[which] takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list, ", ")
pass <user.compound_name_syntax> (and <user.compound_name_syntax>)*:
    user.code_parameter(compound_name_syntax_list)
also pass <user.compound_name_syntax> (and <user.compound_name_syntax>)*:
    user.code_parameter(compound_name_syntax_list, ", ")

returns type <user.type_syntax>:
    user.vscode("jumpToNextSnippetPlaceholder")
    insert(" -> {type_syntax}")
call <user.compound_name_syntax>: user.insert_snippet("{compound_name_syntax}($0)")
return <user.value_syntax>: "return {value_syntax}"
format: user.insert_snippet("f\"$0\"")
if: user.insert_snippet("if $1:\n\t$0")
import <user.compound_name_syntax>: user.insert_snippet("import {compound_name_syntax}\n$0")
class <user.class_syntax>: user.insert_snippet("class {class_syntax}:\n\t$0")
from <user.compound_name_syntax> import <user.name_syntax> ([and] <user.name_syntax>)*:
    user.code_import(compound_name_syntax, name_syntax_list)
map: user.insert_snippet("{{\n\t$1\n\}}")
array: user.insert_snippet("[\n\t$1\n]")
set <user.compound_name_syntax> to: user.insert_snippet("{compound_name_syntax} = $1")
try: user.insert_snippet("try:\n\t$1\nexcept $2:\n\t$3")
op <user.value_syntax> {user.infix_operators} <user.value_syntax>:
    user.insert_snippet("{value_syntax_1} {infix_operators} {value_syntax_2}$0")