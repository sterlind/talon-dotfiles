# Copy paste commands
copy that: edit.copy()
cut that: edit.cut()
paste that: edit.paste()

undo that: edit.undo()
redo that: edit.redo()

# Navigation commands
go <user.navigation_direction>: user.go_direction(navigation_direction)
(select|take) <user.navigation_direction>: user.select_direction(navigation_direction)
copy <user.navigation_direction>: user.copy_direction(navigation_direction)
(delete|clear|chuck) <user.navigation_direction>: user.delete_direction(navigation_direction)

# Line commands
slap:
    key(end)
    key(enter)
zing: edit.indent_less()
indent: edit.indent_more()

# Search commands
scout this: edit.find()
scout next: edit.find_next()