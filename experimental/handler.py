from talon import Module, Context, actions

mod = Module()
ctx = Context()

@mod.action_class
class Actions:
    def code_insert_test(text: str):
        """Inserts a test snippet into the editor"""
        actions.user.rpc_send_message("insert", {
            "text": text,
            "position": {
                "line": 0,
                "character": 0
            }
        })

@ctx.action_class("user")
class UserActions:
    def rpc_handle_message(type: str, contents: object):
        print(f"[{type}] {contents}")