from typing import List
from talon import Module, Context, actions

mod = Module()
ctx = Context()

navigation_types = {
    "CHARACTER": ("left", "right", "up", "down"),
    "WORD": ("ctrl-left", "ctrl-right", "ctrl-up", "ctrl-down"),
    "LINE": ("home", "end", ["up", "home"], ["down", "home"]),
    "PAGE": (None, None, "pageup", "pagedown")
}

mod.list("navigation_type")
ctx.lists["self.navigation_type"] = {
    "char": "CHARACTER",
    "word": "WORD",
    "line": "LINE",
    "page": "PAGE"
}

mod.list("cardinal_direction")
ctx.lists["self.cardinal_direction"] = {
    "left": "0",
    "right": "1",
    "up": "2",
    "down": "3"
}

edit_actions = {
    "go": lambda direction: actions.user.go_direction(direction),
    "take": lambda direction: actions.user.select_direction(direction), 
    "copy": lambda direction: actions.user.copy_direction(direction),
    "chuck": lambda direction: actions.user.delete_direction(direction)
}
mod.list("edit_action")
ctx.lists["self.edit_action"] = [
    "go",
    "take", 
    "copy",
    "chuck"
]

@mod.capture(rule = "[{user.navigation_type}] {user.cardinal_direction}")
def navigation_direction(m) -> List[str]:
    nav_type = getattr(m, "navigation_type", "CHARACTER")
    nav_direction = int(m.cardinal_direction)
    key_list = navigation_types[nav_type][nav_direction]
    return [key_list] if isinstance(key_list, str) else key_list

def prepend_modifier(modifier, keys):
    return [f"{modifier}-{key}" for key in keys]

def apply_key_sequence(keys):
    for key in keys:
        actions.key(key)
    
@mod.action_class
class EditActions:
    def copy():
        """copies selected text"""
        actions.key("ctrl-c")

    def go_direction(direction: List[str]):
        """goes in a particular direction"""
        apply_key_sequence(direction)
    def select_direction(direction: List[str]):
        """selects text in a particular direction"""
        apply_key_sequence(prepend_modifier("shift", direction))
    def copy_direction(direction: List[str]):
        """selects text in a particular direction"""
        apply_key_sequence(prepend_modifier("shift", direction))
        actions.self.copy()