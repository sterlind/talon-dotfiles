tag: user.typescript
-

settings():
    user.constant_formatter = "UPPER_CASE,CAMEL_CASE"
    user.variable_formatter = "CAMEL_CASE"
    user.function_formatter = "CAMEL_CASE"
    user.class_formatter = "HAMMER_CASE"

clap:
    edit.line_end()
    insert(";")
    key("enter")