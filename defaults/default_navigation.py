from talon import Context, actions

ctx = Context()
ctx.tags = ["user.scoped_navigation"]

@ctx.action_class("user")
class UserActions:
    def scoped_default_find(text: str):
        actions.user.find(text)
    
    def scoped_default_find_all(text: str):
        actions.user.find_everywhere(text)
