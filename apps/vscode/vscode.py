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
ctx.tags = ["user.tabs", "user.navigation", "user.find_and_replace", "user.git", "user.scoped_navigation"]

ctx.lists["user.navigation_scope"] = {
    "dock": "document",
    "symbol": "symbol"
}

@mod.action_class
class Actions:
    def insert_snippet(snippet: Union[str, list[str]]):
        "inserts a snippet"
        lines = snippet
        if not isinstance(snippet, list):
            lines = [l.lstrip(" ") for l in snippet.split("\n")]
        snippet = "\n".join(lines)
        actions.user.vscode("editor.action.insertSnippet", {"snippet": snippet})

@ctx.action_class("win")
class WinActions:
    def filename():
        parts = actions.win.title().split(" - ")
        result = parts[0]
        return result if "." else ""
            
@ctx.action_class("user")
class UserActions:
    def go_back():
        actions.user.vscode("workbench.action.navigateBack")
    def go_forward():
        actions.user.vscode("workbench.action.navigateForward")
    
    def tab_close_all():
        actions.user.vscode("workbench.action.closeAllEditors")
    def tab_close_others():
        actions.user.vscode("workbench.action.closeOtherEditors")

    # Git integration:
    def git_status():
        actions.user.vscode("workbench.scm.focus")
    def git_commit():
        actions.user.vscode("git.commitStaged")
    def git_push():
        actions.user.vscode("git.push")
    def git_pull():
        actions.user.vscode("git.pull")
        
    # Navigation scopes:
    def scoped_document_list(text: str):
        actions.user.vscode("workbench.action.quickOpen")
        actions.sleep("50ms")
        actions.insert(text)
    def scoped_document_find(text: str):
        actions.self.scoped_document_list(text)
    def scoped_document_go(text: str):
        actions.self.scoped_document_list(text)
        actions.sleep("250ms")
        actions.key("enter")

    def scoped_symbol_list(text: str):
        actions.user.vscode("workbench.action.gotoSymbol")
        actions.sleep("50ms")
        actions.insert(text)
    def scoped_symbol_list_all(text: str):
        actions.user.vscode("workbench.action.showAllSymbols")
        actions.sleep("50ms")
        actions.insert(text)
    def scoped_symbol_find(text: str):
        actions.self.scoped_symbol_list(text)
    def scoped_symbol_find_all(text: str):
        actions.self.scoped_symbol_list_all(text)
    def scoped_symbol_go(text: str):
        actions.self.scoped_symbol_list(text)
        actions.sleep("250ms")
        actions.key("enter")
    def scoped_symbol_go_all(text: str):
        actions.self.scoped_symbol_list_all(text)
        actions.sleep("250ms")
        actions.key("enter")

    # Find and replace:
    def find_next():
        actions.user.vscode("editor.action.nextMatchFindAction")
    def find_previous():
        actions.user.vscode("editor.action.previousMatchFindAction")
    def find_everywhere(text: str):
        actions.user.vscode("workbench.action.findInFiles")
        if text:
            actions.insert(text)
    def find_toggle_match_by_case():
        actions.key("alt-c")
    def find_toggle_match_by_word():
        actions.key("alt-w")
    def find_toggle_match_by_regex():
        actions.key("alt-r")
    def replace(text: str):
        actions.key("ctrl-h")
        if text:
            actions.insert(text)
    def replace_everywhere(text: str):
        actions.key("ctrl-shift-h")
        if text:
            actions.insert(text)
    def replace_confirm():
        actions.key("ctrl-shift-1")
    def replace_confirm_all():
        actions.key("ctrl-alt-enter")
    def select_previous_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("shift-enter esc")
    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("esc")