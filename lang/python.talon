tag: user.python
-

# make funk <user.text>:
    # user.code_function(text)

# make arg <user.word> of {user.known_types}: user.code_argument(word, user.known_types)
# hello <user.argument>: "{argument}"

# quick [brown]: "quick"
# brown [fox]: "brown fox"

funk <user.name_syntax> takes <user.arguments_syntax>: user.code_function(name_syntax, arguments_syntax)
funk <user.name_syntax>$: user.code_function(name_syntax)