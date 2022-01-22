from talon import Module, actions

mod = Module()

file_naming_conventions = {
    "py": "SNAKE_CASE",
    "talon": "SNAKE_CASE",
    "cs": "HAMMER_CASE"
}

@mod.capture(rule="<user.text> dot {user.extensions}")
def filename(m) -> str:
    file_name = m.text
    if m.extensions in file_naming_conventions:
        file_name = actions.user.format_text(m.text, file_naming_conventions[m.extensions])
    return f"{file_name}.{m.extensions}"