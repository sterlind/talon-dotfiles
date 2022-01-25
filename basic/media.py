from talon import Module, Context, actions

mod = Module()

@mod.action_class
class UserActions:
    def volume_up():
        """Volume increase"""
        actions.key("volup")

    def volume_down():
        """Volume decrease"""
        actions.key("voldown")