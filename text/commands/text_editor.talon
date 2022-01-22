# Copy paste commands
copy that: edit.copy()
cut that: edit.cut()
paste that: edit.paste()

undo that: edit.undo()
redo that: edit.redo()

# Navigation commands
go <user.navigation_direction>: user.go_direction(navigation_direction)
go <user.navigation_direction> <number_small>: user.go_direction(navigation_direction, number_small)
<user.compass_navigation_direction> [<number_small>]: user.go_direction(compass_navigation_direction, number_small or 1)

[go] head: edit.line_start()
[go] tail: edit.line_end()

(select|take) <user.navigation_direction>: user.select_direction(navigation_direction)
(select|take) <user.navigation_direction> <number_small>: user.select_direction(navigation_direction, number_small)
(select|take) <user.compass_navigation_direction> [<number_small>]: user.select_direction(compass_navigation_direction, number_small or 1)
(select|take) all: edit.select_all()
(select|take) last: user.history_select_last_phrase()

copy <user.navigation_direction>: user.copy_direction(navigation_direction)
copy <user.navigation_direction> <number_small>: user.copy_direction(navigation_direction, number_small)
copy all:
    edit.select_all()
    edit.copy()

(delete|clear|chuck) <user.navigation_direction>: user.delete_direction(navigation_direction)
(delete|clear|chuck) <user.navigation_direction> <number_small>: user.delete_direction(navigation_direction, number_small)
(delete|clear|chuck) all:
    edit.select_all()
    edit.delete()
(delete|clear|chuck) last: user.history_clear_last_phrase()

# Matching braces
prince:
    insert("()")
    edit.left()

(angle|diamond|dime):
    insert("<>")
    edit.left()

bracks:
    insert("{}")
    edit.left()

(box|square):
    insert("[]")
    edit.left()

quad:
    insert("\"\"")
    edit.left()

twin:
    insert("''")
    edit.left()

# Line commands
slap:
    key(end)
    key(enter)
zing: edit.indent_less()
indent: edit.indent_more()
push: key("tab")
pull: key("shift-tab")

# Search commands
(hunt|scout) this: edit.find()
(hunt|scout) next: edit.find_next()