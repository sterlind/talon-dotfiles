<user.formatters_code> <user.word_separated_string>$: user.insert_formatted(word_separated_string, formatters_code)
<user.formatters_code> <user.word_separated_string> [over]: user.insert_formatted(word_separated_string, formatters_code)
<user.formatters_code> phrase <user.word_separated_string> [over]: user.insert_formatted(word_separated_string, formatters_code)
<user.formatters_code> format this: user.reformat_selection(formatters_code) 
phrase <user.words>$: "{words}"
phrase <user.words> over: "{words}"
word <word>: "{word}"

<user.capitalized_word>: "{capitalized_word}"
<user.prefixed_word>: "{prefixed_word}"

filename <user.filename>: "{filename}"