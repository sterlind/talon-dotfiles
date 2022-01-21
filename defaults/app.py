from talon import Context, actions

ctx = Context()

@ctx.action_class("app")
class AppActions:
    def window_close():
        actions.key('alt-f4')
    def window_hide():
        actions.key('alt-space n')
    def window_hide_others():
        actions.key('win-d alt-tab')
    def window_next():
        actions.key('alt-`')
    def window_open():
        actions.key('ctrl-n')
    def window_previous():
        actions.key('alt-shift-`')