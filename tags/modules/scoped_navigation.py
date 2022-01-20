from talon import Module

mod = Module()
mod.tag("scoped_navigation")
mod.list("navigation_scope", desc="list of navigation scopes")

@mod.action_class
class UserActions:
    def scoped_list(scope: str, text: str):
        """Lists items of a scope matching the text"""

    def scoped_list_all(scope: str, text: str):
        """Lists all items of a scope matching the text"""
    
    def scoped_find(scope: str, text: str):
        """Searches for items of a scope matching the text"""

    def scoped_find_all(scope: str, text: str):
        """Searches for all items of a scope matching the text"""

    def scoped_go(scope: str, text: str):
        """Goes to the first item of a scope matching the text"""

    def scoped_go_all(scope: str, text: str):
        """Goes to the first item of a scope matching the text"""