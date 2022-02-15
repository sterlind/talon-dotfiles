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
        return self.line < other.line or (self.line == other.line and self.character < other.character)

    def __gt__(self, other):
        return other < self
    
    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
    
    def __str__(self):
        return f"({self.line}, {self.character})"
        
class TreeEditor:
    def __init__(self, tree: Tree, matchers: dict, cursor: Cursor):
        self.tree = tree
        self.matchers = matchers
        self.cursor = cursor

    def move_cursor_to_scope(self, scope: str, selector) -> Cursor:
        if not scope in self.matchers:
            return None
        matcher = self.matchers[scope]
        selected = self.run_matcher(matcher)
        return selector(selected) if selected else None
        
    def get_available_scopes(self) -> set[str]:
        return set(key for key, value in self.matchers.items() if self.run_matcher(value))
    
    def get_nodes_in_range(self, position: Cursor = None):
        position = position or self.cursor

        def walk(node, level):
            for child in node.children:
                if Cursor(child.start_point) <= position and Cursor(child.end_point) >= position:
                    yield from walk(child, level + 1)                
            yield (node, level)

        return map(lambda p: p[0], sorted(walk(self.tree.root_node, 0), key = lambda p: -p[1]))

    def run_matcher(self, matcher, position: Cursor = None) -> Node:
        for node in self.get_nodes_in_range(position):
            result = matcher(node)
            if result:
                return result

    def debug(self):
        nodes_in_range = list(self.get_nodes_in_range())
        cursor = self.tree.walk()
        level = 0
        print(f"Cursor: {self.cursor}")
        while cursor:
            node = cursor.node
            text = repr(node.text.decode("utf8"))
            field_name = cursor.current_field_name() if node.is_named else None
            field_name = f"<{field_name}> " if field_name else ""
            info = f"[{node.type}] {field_name}'{text}' {node.start_point}-{node.end_point}"
            print(" " * level + ("> " if node in nodes_in_range else "* ") + info)
            if cursor.goto_first_child():
                level += 1
            else:
                while not cursor.goto_next_sibling():
                    if not cursor.goto_parent():
                        return
                    level -= 1
        
editor: TreeEditor = None

# def condition_matcher(node):
#     if not node.parent:
#         return None
#     if node.parent.type != "if_statement":
#         return None
#     if node.parent.child_by_field_name("consequence") != node:
#         return node.parent.child_by_field_name("condition")

def condition_matcher(node):
    if not node.parent:
        return
    condition_field = node.parent.child_by_field_name("condition")
    print("siblings:")
    print(node.parent.children)
    print("info:")
    print(f"{repr(node.parent)} {node} {condition_field}")
    if node.parent and node.parent.child_by_field_name("condition") == node:
        return node

def block_matcher(node):
    if node.type == "block":
        return node

matchers = {
    "condition": condition_matcher
}

positions = {
    "start": lambda n: Cursor(n.start_point),
    "end": lambda n: Cursor(n.end_point)
}

for name in matchers.keys():
    mod.tag(name, desc="Grammar context tag")

@mod.action_class
class Actions:
    def lang_insert_at_scope(scope: str, position: str, snippet: str):
        """Inserts a snippet at a particular scope"""
        global editor, positions
        if not editor:
            return

        cursor = editor.move_cursor_to_scope(scope, positions[position])
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
        editor.debug()