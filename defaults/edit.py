from talon import Module, Context, actions, clip
import re

mod = Module()
ctx = Context()

@ctx.action_class("main")
class MainActions:
    def insert(text: str):
        if not text:
            return 
        actions.user.history_insert_phrase(text)
        if isinstance(text, str) and len(text) > 2 and re.search(r"[ /-]|\n", text):
            if paste_text(text):
                return
        actions.next(text)                

def paste_text(text: str):
    """Pastes text and preserves clipboard"""
    with clip.revert():
        clip.set_text(text)

        if clip.text() != text:
            actions.user.notify("Failed to set clipboard")
            print(f"Clipboard: '{clip.text()}'")
            return False

        actions.edit.paste()
        # sleep here so that clip.revert doesn't revert the clipboard too soon
        actions.sleep("150ms")
    return True           

@ctx.action_class("edit")
class EditActions:
    def copy():
        actions.key("ctrl-c")
    def cut():
        actions.key("ctrl-x")
    def paste():
        actions.key("ctrl-v")

    def undo():
        actions.key("ctrl-z")
    def redo():
        actions.key("ctrl-y")

    # Navigation actions
    def left():
        actions.key("left")
    def right():
        actions.key("right")
    def up():
        actions.key("up")
    def down():
        actions.key("down")
    def word_left():
        actions.key("ctrl-left")
    def word_right():
        actions.key("ctrl-right")
    def line_start():
        actions.key("home")
    def line_end():
        actions.key("end")
    def page_down():
        actions.key("pagedown")
    def page_up():
        actions.key("pageup")
    def file_end():
        actions.key("ctrl-end")
    def file_start():
        actions.key("ctrl-home")

    # Selection actions
    def select_none():
        actions.key("esc")
    def select_word():
        actions.edit.right()
        actions.edit.word_left()
        actions.edit.extend_word_right()
    def select_line(n: int=None):
        actions.key("end shift-home")
    def select_all():
        actions.key("ctrl-a")

    # Extension actions
    def extend_left():
        actions.key("shift-left")
    def extend_right():
        actions.key("shift-right")
    def extend_up():
        actions.key("shift-up")
    def extend_down():
        actions.key("shift-down")
    def extend_word_left():
        actions.key("ctrl-shift-left")
    def extend_word_right():
        actions.key("ctrl-shift-right")
    def extend_line_start():
        actions.key("shift-home")
    def extend_line_end():
        actions.key("shift-end")

    # Modification actions
    def delete():
        actions.key("backspace")
    def delete_line():
        actions.edit.select_line()
        actions.edit.delete()        
    def indent_less():
        actions.key("shift-tab")
    def indent_more():
        actions.key("tab")
    
    # Search actions
    def find(text: str = None):
        actions.key("ctrl-f")
    def find_next():
        actions.key("f3")
    
    # Miscellaneous actions
    def selected_text() -> str:
        with clip.capture() as s:
            actions.edit.copy()
        try:
            return s.get()
        except clip.NoChange:
            return ""