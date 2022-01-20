from talon import Module, actions

mod = Module()
mod.tag("scoped_navigation")
mod.list("navigation_scope", desc="list of navigation scopes")

@mod.action_class
class UserActions:
    def scoped_default_list(text: str = None):
        """Default action"""
    def scoped_default_list_all(text: str = None):
        """Default action"""
    def scoped_default_go(text: str = None):
        """Default action"""
    def scoped_default_go_all(text: str = None):
        """Default action"""
    def scoped_default_find(text: str = None):
        """Default action"""
    def scoped_default_find_all(text: str = None):
        """Default action"""

    def scoped_document_list(text: str = None):
        """Default action"""
    def scoped_document_list_all(text: str = None):
        """Default action"""
    def scoped_document_go(text: str = None):
        """Default action"""
    def scoped_document_go_all(text: str = None):
        """Default action"""
    def scoped_document_find(text: str = None):
        """Default action"""
    def scoped_document_find_all(text: str = None):
        """Default action"""

    def scoped_symbol_list(text: str = None):
        """Default action"""
    def scoped_symbol_list_all(text: str = None):
        """Default action"""
    def scoped_symbol_go(text: str = None):
        """Default action"""
    def scoped_symbol_go_all(text: str = None):
        """Default action"""
    def scoped_symbol_find(text: str = None):
        """Default action"""
    def scoped_symbol_find_all(text: str = None):
        """Default action"""
        
    def scoped_navigation(action: str, scope: str, all: str = "", text: str = None):
        """Does a scoped navigation command"""
        suffix = "_all" if all else ""
        function_name = f"scoped_{scope}_{action}{suffix}"
        action = getattr(actions.user, function_name, None)
        if not action:
            print(f"no navigation action {function_name} defined!")
            return
        print(repr(action))
        action(text)
        