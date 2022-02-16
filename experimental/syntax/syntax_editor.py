from dataclasses import dataclass
import logging
from pathlib import Path
from talon import Module, Context, actions
from tree_sitter import Language, Parser, Tree, Node
from .analyzer import Analyzer, Config, parse_config

mod = Module()
ctx = Context()

CONFIG_PATH = Path(__file__).parent.parent / "config"

def load_language(name: str) -> Analyzer:
    lang = Language("build/languages.dll", name)
    config = parse_config(CONFIG_PATH / f"{name}.toml")
    return Analyzer(lang, config)

class EditorState:
    def __init__(self, analyzers: dict[str, Analyzer]):
        self.scopes = {}
        self.analyzers = analyzers

    def receive(self, language: str, text: str, cursor: tuple[int, int]):
        self.scopes = self.analyzers[language].get_scopes(text, cursor)
    
    def send_replace_message(self, scope: str, snippet: str):
        node = self.scopes[scope]
        text = snippet.replace("$$", node.text.decode("utf8").strip())

        actions.user.rpc_send_message("replaceRange", {
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
        })

    def get_tags(self):
        return [f"user.{name}" for name in self.scopes.keys()]
    
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

@ctx.action_class("user")
class UserActions:
    def rpc_handle_message(type: str, contents: object):
        global state
        if type != "editorText":
            # actions.next()
            return

        state.receive(
            "python", # for now
            contents["text"],
            (contents["cursor"]["line"], contents["cursor"]["character"]))

        ctx.tags = state.get_tags()
        logging.info(f"Enabled the following contexts: {ctx.tags}")