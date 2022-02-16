tag: user.primitive_value
-
string <user.text>: user.code_replace_target("primitive_value", "\"{text}\"")
<number>: user.code_replace_target("primitive_value", "{number}")