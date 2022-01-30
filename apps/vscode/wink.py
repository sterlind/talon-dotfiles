from talon import fs, resource, Module, Context
from tempfile import gettempdir
from pathlib import Path
import json

ctx = Context()
ctx.matches = r"""
app: vscode
"""

COMMUNICATION_PATH = Path(gettempdir()) / "wink"
VOCAB_PATH = Path(COMMUNICATION_PATH / "vocab.json")

if not COMMUNICATION_PATH.exists():
    COMMUNICATION_PATH.mkdir(parents = True)

if not VOCAB_PATH.exists():
    VOCAB_PATH.touch()

def read_vocab_from_file(path: str) -> list[str]:
    with resource.open(path, "r") as f:
        contents = []
        try:
            contents = json.loads(f.read())
        except Exception as ex:
            print(repr(ex))            
        print("refreshed contents:")
        print(repr(contents))
        return contents
        
ctx.lists["user.symbols"] = read_vocab_from_file(VOCAB_PATH)
