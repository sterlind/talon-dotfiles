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

[declare] (const|constant) <user.compound_name_syntax> (to|is):
    user.code_statement_variable_declare(compound_name_syntax, "const")
[declare] (const|constant) <user.compound_name_syntax> (to|is) <user.value_syntax>:
    user.code_statement_variable_declare(compound_name_syntax, "const", value_syntax)

let <user.compound_name_syntax> (be|is):
    user.code_statement_variable_declare(compound_name_syntax, "let")
let <user.compound_name_syntax> (be|is) <user.value_syntax>:
    user.code_statement_variable_declare(compound_name_syntax, "let", value_syntax)