import logging
from tree_sitter import Language, Parser, Tree, Node
from talon import Module, Context, actions

PYTHON_LANGUAGE = Language("build/languages.dll", "python")

parser = Parser()
parser.set_language(PYTHON_LANGUAGE)

mod = Module()
ctx = Context()

class Cursor:
    def __init__(self, position: tuple[int, int]):
        self.line, self.character = position
    
    def __eq__(self, other):
        return self.line == other.line and self.character == other.character
    
    def __ne__(self, other):
        return not (self == other)
        
    def __lt__(self, other):
        return self.line < other.line or self.character < other.character

    def __gt__(self, other):
        return other < self
    
    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
        
class TreeEditor:
    def __init__(self, tree: Tree, matchers: dict, cursor: Cursor):
        self.tree = tree
        self.matchers = matchers
        self.cursor = cursor

    def move_cursor_to_scope(self, scope: str) -> Cursor:
        if not scope in self.matchers:
            return None
        matcher = self.matchers[scope]
        node = self.get_node_at_position()
        while node:
            selected = matcher(node)
            if selected:
                return Cursor(selected.end_point)                
            node = node.parent
        return None
    
    def get_node_at_position(self, position: Cursor = None) -> Node:
        position = position or self.cursor
        def walk(node):
            for child in node.children:
                if Cursor(child.start_point) <= position and Cursor(child.end_point) >= position:
                    return walk(child)
            return node
        
        return walk(self.tree.root_node)

    def get_available_scopes(self) -> set[str]:
        node = self.get_node_at_position()
        def walk_up(matcher, node):
            while node:
                if matcher(node):                    
                    return True                
                node = node.parent
            return False
                    
        return set(key for key, value in self.matchers.items() if walk_up(value, node))

editor: TreeEditor = None
matchers = {}
matchers["if_condition"] = lambda n: n.child_by_field_name("condition") if n.type == "if_statement" else None

for name in matchers.keys():
    mod.tag(name, desc="Grammar context tag")

@mod.action_class
class Actions:
    def lang_insert_at_scope(scope: str, snippet: str):
        """Inserts a snippet at a particular scope"""
        global editor
        if not editor:
            return

        cursor = editor.move_cursor_to_scope(scope)
        actions.user.rpc_send_message("insert", {
            "text": snippet,
            "position": {
                "line": cursor.line,
                "character": cursor.character
            }
        })

@ctx.action_class("user")
class UserActions:
    def rpc_handle_message(type: str, contents: object):
        global editor, parser, matchers
        if type != "editorText":
            # actions.next()
            return

        tree = parser.parse(contents["text"].encode("utf8"))
        editor = TreeEditor(tree, matchers, Cursor((contents["cursor"]["line"], contents["cursor"]["character"])))
        scopes = editor.get_available_scopes()
        ctx.tags = list(f"user.{scope}" for scope in scopes)
        logging.info(f"Enabled the following contexts: {ctx.tags}")