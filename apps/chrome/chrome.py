from talon import Module, Context, actions, app

ctx = Context()
mod = Module()
mod.apps.chrome = """
app.name: Google Chrome
app.exe: chrome.exe
"""

mod.apps.microsoft_edge = """
os: windows
and app.name: msedge.exe
os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: msedge.exe
"""

ctx.matches = r"""
app: chrome
app: microsoft_edge
"""

ctx.tags = ["user.tabs", "user.navigation", "browser"]

@ctx.action_class("browser")
class BrowserActions:
    def focus_address():
        actions.key("ctrl-l")

@ctx.action_class("user")
class UserActions:
    # Tab support
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-{number}")

    def tab_final():
        actions.key("ctrl-9")

    # Navigation support
    def go_back():
        actions.key("alt-left")
    
    def go_forward():
        actions.key("alt-right")

    # The following require mapping in the vimium extension:
    def tab_close_others():
        actions.key("ctrl-alt-o")

    def tab_close_left():
        actions.key("ctrl-alt-l")

    def tab_close_right():
        actions.key("ctrl-alt-r")