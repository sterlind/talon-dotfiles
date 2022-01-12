from talon import Module, Context, actions

mod = Module()
mod.mode("dictation")

@mod.action_class
class Actions:
    def dictation_insert(text: str) -> str:
        """inserts dictated text"""
        pass