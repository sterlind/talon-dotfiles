from talon import Module, actions
from typing import Union

mod = Module()

@mod.action_class
class Actions:
    def insert_formatted_snippet(snippet: str):
        """Insert a formatted snippet"""
        
    def insert_snippet(snippet: Union[str, list[str]]):
        "Inserts a snippet"
        lines = snippet
        if not isinstance(snippet, list):
            lines = [l.lstrip(" ") for l in snippet.split("\n")]
        actions.user.insert_formatted_snippet("\n".join(lines))