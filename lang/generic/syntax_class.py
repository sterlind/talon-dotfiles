from talon import Module, actions, settings

mod = Module()
mod.tag("class_language")

mod.setting("class_formatter", str)

@mod.capture(rule="<user.raw_name_syntax>")
def class_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.class_formatter"))

@mod.action_class
class UserActions:
    def code_declare_class(name: str):
        """Declares a class"""

    def code_declare_constructor():
        """Inserts a constructor snippet"""