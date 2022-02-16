tag: user.primitive_value
-
string <user.text>: user.code_replace_target("primitive_value", "\"$$\"")
<number>: user.code_replace_target("primitive_value", "$$")