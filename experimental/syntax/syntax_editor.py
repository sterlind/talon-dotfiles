import logging
from pathlib import Path
from typing import Union
from talon import Module, Context, actions
from talon.grammar import Phrase
from tree_sitter import Language, Parser, Tree, Node
from .analyzer import Analyzer, Config, parse_config

CONFIG_PATH = Path(__file__).parent.parent / "config"

def load_language(name: str) -> Analyzer:
    lang = Language("build/languages.dll", name)
    config = parse_config(CONFIG_PATH / f"{name}.toml")
    return Analyzer(lang, config)

mod = Module()
ctx = Context()

mod.tag("suggestions_active")

mod.list("top_level_symbols")
ctx.lists["user.top_level_symbols"] = []

mod.list("suggestions")
ctx.lists["user.suggestions"] = []

class EditorState:
    def __init__(self, analyzers: dict[str, Analyzer]):
        self.scopes = {}
        self.analyzers = analyzers

    def receive(self, language: str, text: str, cursor: tuple[int, int]):
        self.scopes = self.analyzers[language].get_scopes(text, cursor)
        self._update_tags()
    
    def send_replace_message(self, scope: str, snippet: str):
        node = self.scopes[scope]
        text = snippet.replace("$$", node.text.decode("utf8").strip())

        message = {
            "range": {
                "start": {
                    "line": node.start_point[0],
                    "character": node.start_point[1]
                },
                "end": {
                    "line": node.end_point[0],
                    "character": node.end_point[1]
                },
            },
            "text": text
        }

        reply = actions.user.rpc_send_message("replaceRange", message)
        state.receive(
            "python", # for now
            reply["text"],
            (reply["cursor"]["line"], reply["cursor"]["character"]))    

    def code_start_completion(self):
        suggestions = actions.user.rpc_send_message("startCompletion", None)
        if not suggestions:
            logging.warning("No suggestions available, aborting.")
            return

        ctx.tags = ["user.suggestions_active"]
        ctx.lists["user.suggestions"] = suggestions
    
    def code_finish_completion(self, label):
        actions.user.rpc_send_message("insertTextAtCursor", {
            "text": label
        })
        self.code_abandon_completion()

    def code_abandon_completion(self):
        ctx.tags = []
        self._update_tags()
    
    def _update_tags(self):
        if "user.suggestions_active" in ctx.tags:
            logging.warning(f"Suggestions were active, ignoring.")
            return

        ctx.tags = [f"user.{name}" for name in self.scopes.keys()]
        logging.info(f"Enabled the following contexts: {ctx.tags}")

def make_state():
    analyzers = {
        name: load_language(name) for name in [
            "python"
        ]
    }

    return EditorState(analyzers)

state = make_state()        

@mod.action_class
class Actions:
    def code_replace_target(scope: str, snippet: str):
        """Replaces a scope node's contents with the provided snippet."""
        global state
        state.send_replace_message(scope, snippet)

    def code_edit(scope: str, snippet: str, next: Union[Phrase, str]):
        """Replaces a scope node's contents with the provided snippet."""
        global state
        state.send_replace_message(scope, snippet)
        if next:
            actions.user.rephrase(next)

    def code_start_completion():
        """Starts a completion suggestion"""
        global state
        state.code_start_completion()

    def code_abandon_completion():
        """Forsakes a completion suggestion"""
        global state
        state.code_abandon_completion()
    
    def code_finish_completion(label: str):
        """Finishes a completion suggestion"""
        global state
        state.code_finish_completion(label)

def update_editor_text(contents):
    global state
    state.receive(
        "python", # for now
        contents["text"],
        (contents["cursor"]["line"], contents["cursor"]["character"]))

def update_symbols(contents):
    ctx.lists["user.top_level_symbols"] = contents
    logging.info(f"Symbols updated: {contents}")

handlers = {
    "editorText": update_editor_text,
    "symbols": update_symbols
}

@ctx.action_class("user")
class UserActions:
    def rpc_handle_message(type: str, contents: object):
        if not type in handlers:
            logging.warning(f"Unable to handle message type {type}")
            return
        
        handlers[type](contents)