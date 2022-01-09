tag: user.python
-

# make funk <user.text>:
    # user.code_function(text)

# make arg <user.word> of {user.known_types}: user.code_argument(word, user.known_types)
# hello <user.argument>: "{argument}"

# quick [brown]: "quick"
# brown [fox]: "brown fox"

funk <user.name_syntax> takes <user.parameters_syntax>: user.code_function(name_syntax, parameters_syntax)
funk <user.name_syntax>$: user.code_function(name_syntax)
call <user.compound_name_syntax>: user.insert_snippet("{compound_name_syntax}($0)")