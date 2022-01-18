from talon import Module, actions

mod = Module()

MAX_PHRASES = 100
history = []

@mod.action_class
class Actions:
    def history_insert_phrase(text: str):
        """Inserts a phrase into the history"""
        global history
        while MAX_PHRASES > 100:                        
            history = history[:100]
        history.insert(0, text)
    
    def history_select_last_phrase() -> str:
        """Selects the last phrase"""
        global history
        if not history:
            return None
        actions.edit.select_none()
        for _ in range(len(history[0])):
            actions.edit.extend_left()
        selected = actions.edit.selected_text()            
        return selected
            
    def history_clear_last_phrase():
        """Clears the last phrase"""
        global history
        selected = actions.self.history_select_last_phrase()
        if not history:
            return            
        if selected != history[0]:
            history.clear()
            return            
        actions.edit.delete()
        history.pop(0)