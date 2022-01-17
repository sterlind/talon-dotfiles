from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def history_insert_phrase(text: str):
        