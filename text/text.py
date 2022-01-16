from talon import Module, actions
from typing import List

mod = Module()

@mod.action_class
class Actions:
    def insert_many(strings: List[str]) -> None:
        "Insert multiple strings"
        for string in strings:
            actions.insert(string)
    def insert_formatted(text: str, format: str) -> None:
        "Insert formatted"
        actions.insert(actions.user.format_text(text, format))