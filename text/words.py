from talon import Module, Context, actions, grammar
import re
from typing import List
from functools import reduce

mod = Module()
ctx = Context()

@mod.capture(rule="(abbreviate|brief|abbrieve) {user.abbreviation}")
def abbreviated_word(m) -> str:
    return m.abbreviation
    
@mod.capture(rule="spell (<user.letter>)+ [over]")
def spelled_word(m) -> str:
    return "".join(m.letter_list)

@mod.capture(rule = "cap <user.unmodified_word>")
def capitalized_word(m) -> str:
    "Capitalized modifier for words (put other modifiers here)"
    return m.unmodified_word.capitalize()

@mod.capture(rule="({self.vocabulary} | <user.abbreviated_word> | <user.spelled_word> | <word>)")
def unmodified_word(m) -> str:
    "Single word"
    return str(m)

@mod.capture(rule = "<user.capitalized_word> | <user.unmodified_word>")
def word(m) -> str:
    "Single word"
    return str(m)
