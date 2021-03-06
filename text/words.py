from talon import Module, Context

mod = Module()
ctx = Context()

@mod.capture(rule="dot {user.extensions}")
def file_extension(m) -> str:
    return f".{m.extensions}"

@mod.capture(rule="(num|number) <number>")
def number_word(m) -> str:
    return str(m.number)

@mod.capture(rule="(abbreviate|brief|abbrieve) {user.abbreviations}")
def abbreviated_word(m) -> str:
    return m.abbreviations
    
@mod.capture(rule="spell (<user.letter>)+ [over]")
def spelled_word(m) -> str:
    return "".join(m.letter_list)

@mod.capture(rule="word <word>")
def literal_word(m) -> str:
    return m.word

@mod.capture(rule = "cap <user.unmodified_word>")
def capitalized_word(m) -> str:
    "Capitalized modifier for words (put other modifiers here)"
    return m.unmodified_word.capitalize()

@mod.capture(rule="<user.abbreviated_word> | <user.spelled_word> | <user.number_word> | <user.literal_word>")
def prefixed_word(m) -> str:
    """Prefixed word (keyword occurs before)"""
    return str(m)

@mod.capture(rule="(<user.prefixed_word> | <user.file_extension> | {user.vocabulary} | <word>)")
def unmodified_word(m) -> str:
    "Single word"
    return str(m)
    
@mod.capture(rule = "<user.capitalized_word> | <user.unmodified_word>")
def word(m) -> str:
    "Single word"
    return str(m)
