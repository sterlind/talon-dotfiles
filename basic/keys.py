from talon import Context, Module
from ..util import merge

mod = Module()
ctx = Context()

phonetic_alphabet = """
    air
    bat
    car
    drum
    each
    fine
    gust
    harp
    sit
    june
    crunch
    look
    made
    near
    odd
    pit
    quench
    red
    sun
    trap
    urge
    vest
    whale
    plex
    yell
    zap
""".split()

alphabet_letters = "abcdefghijklmnopqrstuvwxyz"

phonetic_digits = """
    zero
    one
    two
    three
    four
    five
    six
    seven
    eight
    nine
""".split()

mod.list("letter", desc="Phonetic alphabet")
ctx.lists["self.letter"] = dict(zip(phonetic_alphabet, alphabet_letters))

mod.list("key_number", desc="Digits")
ctx.lists["self.key_number"] = dict(zip(phonetic_digits, [str(k) for k in range(10)]))

mod.list("key_arrow", desc="Arrow keys")
ctx.lists["self.key_arrow"] = {"up", "down", "left", "right"}

mod.list("key_special", desc="All special keys")
ctx.lists["self.key_special"] = merge(
    {
        "enter",
        "tab",
        "delete",
        "backspace",
        "home",
        "end",
        "insert",
        "escape",
        "menu",
    },
    {
        "page up":      "pageup",
        "page down":    "pagedown",
        "print screen": "printscr",
    }
)

mod.list("key_modifier", desc="All modifier keys")
ctx.lists["self.key_modifier"] = {
    "alt":          "alt",
    "control":      "ctrl",
    "shift":        "shift",
    "super":        "super",
}

# Symbols available in command mode, but NOT during dictation.
mod.list("key_symbol", desc="All symbols from the keyboard")
ctx.lists["self.key_symbol"] = {
    "void":             " ",
    "dot":              ".",
    "comma":            ",",
    "stack":            ":",
    "semi":             ";",
    "dash":             "-",
    "score":            "_",

    "bang":             "!",
    "hash":             "#",
    "star":             "*",
    "dollar":           "$",
    "percent":          "%",
    "question":         "?",
    "amper":            "&",
    "at sign":          "@",

    "dubquote":            '"',
    "quote":       "'",
    "brick":            "`",

    "slash":            "/",
    "backslash":        "\\",
    "pipe":             "|",

    "paren":            "(",
    "rearen":           ")",
    "brace":            "{",
    "race":             "}",
    "square":           "[",
    "rare":             "]",
    "angle":            "<",
    "rangle":           ">",

    "caret":            "^",
    "tilde":            "~",
    "plus":             "+",
    "minus":            "-",
    "equals":           "=",
}

@mod.capture(rule="{self.key_modifier}+")
def key_modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.key_modifier_list)

@mod.capture(
    rule="{self.letter} | {self.key_number} | {self.key_symbol} | {self.key_special} | {self.key_arrow}"
)
def key_unmodified(m) -> str:
    "A single key with no modifiers"
    if m[0] == " ":
        return "space"
    return m[0]

@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    "One letter key"
    return m.letter

@mod.capture(rule="{self.key_number}")
def key_number(m) -> str:
    "One number key"
    return m.key_number

@mod.capture(rule="({self.letter} | {self.key_number} | {self.key_symbol})")
def any_alphanumeric_key(m) -> str:
    "any alphanumeric key"
    return str(m)