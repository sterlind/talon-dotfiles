<user.formatters_code> <user.words>$: user.insert_formatted(words, formatters_code)
<user.formatters_code> <user.words> [over]: user.insert_formatted(words, formatters_code)
phrase <user.words>$: "{words}"
phrase <user.words> over: "{words}"
word <user.word>: "{word}"
cap <user.word>: user.insert_formatted(word, "PROPER_CASE")
slap:
    key(end)
    key(enter)