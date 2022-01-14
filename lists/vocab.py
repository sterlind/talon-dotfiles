from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="Vocabulary")
ctx.lists["self.vocabulary"] = []

mod.list("abbreviation", desc="Maps full words to their abbreviations")
ctx.lists["self.abbreviation"] = {
    "context": "ctx",
    "module": "mod",
    "regex": "re",
    "control": "ctrl",
    "navigation": "nav",
    "integer": "int",
    "character": "char"
}