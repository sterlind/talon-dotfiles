tag: user.primitive_value
-
string <user.text>: user.code_replace_target("primitive_value", "\"{text}\"")
<number>: user.code_replace_target("primitive_value", "{number}")
^{user.top_level_symbols} [<phrase>]: user.code_edit("primitive_value", "{top_level_symbols}", phrase or "")
^{user.top_level_symbols} dot [<phrase>]:
    user.code_replace_target("primitive_value", "{top_level_symbols}.")
    user.code_start_completion()
    user.rephrase(phrase)