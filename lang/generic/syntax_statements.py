from talon import Module, actions, settings

mod = Module()
mod.tag("statement_language")

mod.setting("function_formatter", str)

@mod.capture(rule="<user.raw_name_syntax>")
def function_name_syntax(m) -> str:
    return actions.user.format_text(m.raw_name_syntax, settings.get("user.function_formatter"))

@mod.capture(rule="<user.name_syntax>")
def parameter_syntax(m) -> str:
    return m.name_syntax

@mod.capture(rule="<user.parameter_syntax> ([and] <user.parameter_syntax>)*")
def parameters_syntax(m) -> list[str]:
    return m.parameter_syntax_list

@mod.action_class
class UserActions:
    def code_declare_import(module: str, named_imports: list[str] = None):
        """Inserts an import statement"""
        
    def code_declare_function(name: str):
        """Declares a function"""