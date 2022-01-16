from talon import Module, actions
from typing import List

mod = Module()

@mod.action_class
class Actions:
    def insert_formatted(text: str, format: str) -> None:
        "Insert formatted"
        actions.insert(actions.user.format_text(text, format))
    
    def reformat_selection(formatters: str):
        """Reformats the selected text"""
        selected = actions.edit.selected_text()
        if not selected:
            return
        actions.insert(actions.user.reformat_text(selected, formatters))

    def reformat_text(text: str, formatters: str) -> str:
        """Reformat the text. Used by Cursorless"""
        lines = text.split("\n")
        for i in range(len(lines)):
            unformatted = actions.user.unformat_text(lines[i])
            lines[i] = actions.user.format_text(unformatted, formatters)
        return "\n".join(lines)