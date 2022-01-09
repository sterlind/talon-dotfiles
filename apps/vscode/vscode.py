from typing import Union
from talon import Context, Module, actions

ctx = Context()
mod = Module()
mod.apps.vscode = """
os: windows
and app.name: Visual Studio Code
os: windows
and app.exe: Code.exe
"""

ctx.matches = r"""
app: vscode
"""
ctx.tags = ["user.tabs"]

@mod.action_class
class Actions:
    def insert_snippet(snippet: Union[str, list[str]]):
        "inserts a snippet"
        lines = snippet
        if not isinstance(snippet, list):
            lines = [l.lstrip(" ") for l in snippet.split("\n")]
        snippet = "\n".join(lines)
        actions.user.vscode("editor.action.insertSnippet", {"snippet": snippet})