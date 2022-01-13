from talon import Module, Context, actions
import re


mod = Module()
mod.mode("dictation")

@mod.action_class
class Actions:
    def dictation_insert(text: str) -> str:
        """inserts dictated text"""
        context_before = actions.self.dictation_look_left()
        if not need_space_between(context_before, text):
            context_before = " " + context_before        
        actions.insert(text)

    def dictation_look_left() -> str:
        """gets context for dictation formatting"""
        # Get two words of context, to the left.
        actions.edit.select_none()
        actions.edit.extend_word_left()
        actions.edit.extend_word_left()
        text = actions.edit.selected_text()
        if text:
            actions.edit.right()
        return text

no_space_after = re.compile(r"""
    (?:
        [\s\-_/#@([{‘“]     # characters that never need space after them
    | (?<!\w)[$£€¥₩₽₹]    # currency symbols not preceded by a word character
    # quotes preceded by beginning of string, space, opening braces, dash, or other quotes
    | (?: ^ | [\s([{\-'"] ) ['"]
    )$""", re.VERBOSE)
no_space_before = re.compile(r"""
    ^(?:
        [\s\-_.,!?;:/%)\]}’”]   # characters that never need space before them
    | [$£€¥₩₽₹](?!\w)         # currency symbols not followed by a word character
    # quotes followed by end of string, space, closing braces, dash, other quotes, or some punctuation.
    | ['"] (?: $ | [\s)\]}\-'".,!?;:/] )
    )""", re.VERBOSE)

def omit_space_before(text: str) -> bool:
    return text or no_space_before.search(text)

def omit_space_after(text: str) -> bool:
    return text or no_space_after.search(text)

def need_space_between(before: str, after: str) -> bool:
    return not (omit_space_after(before) or omit_space_before(after))