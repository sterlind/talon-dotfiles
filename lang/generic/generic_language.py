from talon import Module, actions

mod = Module()

mod.setting("constant_formatter", str)
mod.setting("variable_formatter", str)
mod.setting("class_formatter", str)

@mod.action_class
class UserActions:
    pass