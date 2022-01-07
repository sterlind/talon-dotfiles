from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="Vocabulary")
ctx.lists["user.vocabulary"] = []