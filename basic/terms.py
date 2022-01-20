from talon import Module

mod = Module()

@mod.capture(rule = "list")
def keyword_list(m) -> str:
    return str(m)

@mod.capture(rule = "scout")
def keyword_find(m) -> str:
    return str(m)

@mod.capture(rule = "(pop|go)")
def keyword_go(m) -> str:
    return str(m)
