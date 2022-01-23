tag: user.python
-

settings():
    user.constant_formatter = "UPPER_CASE,SNAKE_CASE"
    user.variable_formatter = "SNAKE_CASE"
    user.function_formatter = "SNAKE_CASE"
    user.class_formatter = "HAMMER_CASE"

make map: user.insert_snippet("{{\n\t$1\n}}")
make array: user.insert_snippet("[\n\t$1\n]")
make pass: insert("pass")