from talon import Context, Module

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

alphabet_letters = "abcdefghijklmnopqrstuvwxyz"

alphabet = dict(zip(phonetic_alphabet, alphabet_letters))

mod = Module()
mod.list("letter", desc="Phonetic alphabet")
mod.list("number_key", desc="Digits")

@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    "One letter key"
    return m.letter

@mod.capture(rule="{self.number_key}")
def number_key(m) -> str:
    "One number key"
    return m.number_key

ctx = Context()
ctx.lists["self.letter"] = alphabet
ctx.lists["self.number_key"] = dict(zip(phonetic_digits, [str(k) for k in range(10)]))