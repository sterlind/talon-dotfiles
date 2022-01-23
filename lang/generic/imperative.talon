tag: user.imperative_language
-

if [call]: user.code_block_if()
if <user.logic_syntax>: user.code_block_if(logic_syntax)

make for: user.code_block_for()
for <user.name_syntax> in: user.code_block_for(name_syntax)
for <user.name_syntax> in <user.value_syntax>: user.code_block_for(name_syntax, value_syntax)

make while: user.code_block_while()
while <user.value_syntax>: user.code_block_while(value_syntax)

make try: user.code_block_try_catch()

with as <user.name_syntax>: user.code_block_scope(name_syntax)

make pass: insert("pass")