from typing import List
from talon import Module, Context, actions

mod = Module()
ctx = Context()

navigation_types = {
    "CHARACTER": ("left", "right", "up", "down"),
    "WORD": ("ctrl-left", "ctrl-right", "ctrl-up", "ctrl-down"),
    "LINE": ("home", "end", ["up", "home"], ["down", "home"]),
    "PAGE": (None, None, "pageup", "pagedown"),
    "WAY": (["home", "home"], ["end", "end"], "ctrl-home", "ctrl-end")
}

mod.list("navigation_type")
ctx.lists["self.navigation_type"] = {
    "char": "CHARACTER",
    "word": "WORD",
    "line": "LINE",
    "way": "WAY",
    "page": "PAGE"
}

mod.list("cardinal_direction")
ctx.lists["self.cardinal_direction"] = {
    "left": "0",
    "right": "1",
    "up": "2",
    "down": "3"
}

mod.list("compass_direction")
ctx.lists["self.compass_direction"] = {
    "west": "0",
    "east": "1",
    "north": "2",
    "south": "3"
}

@mod.capture(rule = "[{user.navigation_type}] {user.cardinal_direction}")
def navigation_direction(m) -> List[str]:
    nav_type = getattr(m, "navigation_type", "CHARACTER")
    nav_direction = int(m.cardinal_direction)
    key_list = navigation_types[nav_type][nav_direction]
    return [key_list] if isinstance(key_list, str) else key_list

@mod.capture(rule = "{user.compass_direction} [{user.navigation_type}]")
def compass_navigation_direction(m) -> List[str]:
    nav_type = getattr(m, "navigation_type", "CHARACTER")
    nav_direction = int(m.compass_direction)
    key_list = navigation_types[nav_type][nav_direction]
    return [key_list] if isinstance(key_list, str) else key_list

def prepend_modifier(modifier, keys):
    return [f"{modifier}-{key}" for key in keys]

def apply_key_sequence(keys, count):
    for _ in range(count):        
        for key in keys:
            actions.key(key)        

@mod.action_class
class TextNavigationActions:
    def go_direction(direction: List[str], count: int = 1):
        """goes in a particular direction"""
        apply_key_sequence(direction, count)
    def select_direction(direction: List[str], count: int = 1):
        """selects text in a particular direction"""
        apply_key_sequence(prepend_modifier("shift", direction), count)
    def copy_direction(direction: List[str], count: int = 1):
        """selects text in a particular direction"""
        actions.self.select_direction(direction, count)
        actions.edit.copy()
    def delete_direction(direction: List[str], count: int = 1):
        """deletes text in a particular direction"""
        actions.self.select_direction(direction, count)
        actions.edit.delete()