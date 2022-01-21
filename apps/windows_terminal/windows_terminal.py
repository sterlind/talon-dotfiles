from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.windows_terminal = """
os: windows
and app.exe: WindowsTerminal.exe
"""

ctx.matches = r"""
app: windows_terminal
"""

ctx.tags = ["user.tabs"]

@ctx.action_class("app")
class AppActions:
    def tab_previous():
        actions.key("ctrl-shift-tab")
    def tab_next():
        actions.key("ctrl-tab")

@ctx.action_class("edit")
class EditActions:
    def copy():
        actions.key("ctrl-shift-c")
    def paste():
        actions.key("ctrl-shift-v")