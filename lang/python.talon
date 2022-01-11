tag: user.python
-

# make funk <user.text>:
    # user.code_function(text)

# make arg <user.word> of {user.known_types}: user.code_argument(word, user.known_types)
# hello <user.argument>: "{argument}"

# quick [brown]: "quick"
# brown [fox]: "brown fox"

funk <user.name_syntax>:
    user.insert_snippet("def {name_syntax}($1)$2:")
takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list)
also takes <user.parameter_syntax> (and <user.parameter_syntax>)*:
    user.code_parameter(parameter_syntax_list, ", ")
returns type <user.type_syntax>:
    user.vscode("jumpToNextSnippetPlaceholder")
    insert(" -> {type_syntax}")
# funk <user.name_syntax> [takes <user.parameters_syntax>] [returns <user.type_syntax>]:
    # user.code_function(name_syntax, parameters_syntax or None, type_syntax or None)
# funk <user.name_syntax>$: user.code_function(name_syntax)
call <user.compound_name_syntax>: user.insert_snippet("{compound_name_syntax}($0)")
return <user.value_syntax>: "return {value_syntax}"
format: user.insert_snippet("f\"$0\"")
import <user.compound_name_syntax>: user.insert_snippet("import {compound_name_syntax}\n$0")
from <user.compound_name_syntax> import <user.name_syntax> ([and] <user.name_syntax>)*:
    user.insert_snippet("from {compound_name_syntax} import {name_syntax}\n$0") 
# type <user.type_syntax>: "{type_syntax}"
map: user.insert_snippet("{{\n\t$1\n\}}")
array: user.insert_snippet("[\n\t$1\n]")
set <user.compound_name_syntax> to: user.insert_snippet("{compound_name_syntax} = $1")
try: user.insert_snippet("try:\n\t$1\nexcept $2:\n\t$3")