<user.formatters_code> <user.word_separated_string>$: user.insert_formatted(word_separated_string, formatters_code)
<user.formatters_code> <user.word_separated_string> [over]: user.insert_formatted(word_separated_string, formatters_code)
phrase <user.words>$: "{words}"
phrase <user.words> over: "{words}"
word <user.word>: "{word}"
cap <user.word>: user.insert_formatted(word, "PROPER_CASE")
slap:
    key(end)
    key(enter)