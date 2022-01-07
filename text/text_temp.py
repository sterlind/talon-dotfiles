from talon import Module, Context, actions
from typing import List

mod = Module()
ctx = Context()

@mod.action_class
class Actions:
    def insert_many(strings: List[str]) -> None:
        "Insert multiple strings"
        for string in strings:
            actions.insert(string)