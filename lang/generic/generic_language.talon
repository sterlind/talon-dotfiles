tag: user.generic_language
-

# Comments
document <user.text>$:
    result = user.format_text(text, "SENTENCE_CASE")
    insert("\"\"\"{result}\"\"\"")
explain <user.text>$:
    result = user.format_text(text, "SENTENCE_CASE")
    insert("# {result}")
