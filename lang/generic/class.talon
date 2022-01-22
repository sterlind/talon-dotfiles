tag: user.class_language
-

make class <user.class_syntax>: user.insert_snippet("class {class_syntax}:\n\t$0")

constructor: user.insert_snippet("def __init__($1)$2:")