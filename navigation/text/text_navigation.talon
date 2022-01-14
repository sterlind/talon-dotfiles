tag: user.navigation
-

copy that: edit.copy()
cut that: edit.cut()
paste that: edit.paste()

undo that: edit.undo()
redo that: edit.redo()

go <user.navigation_direction>: user.go_direction(navigation_direction)
(select|take) <user.navigation_direction>: user.select_direction(navigation_direction)
copy <user.navigation_direction>: user.copy_direction(navigation_direction)
(delete|clear) <user.navigation_direction>: user.delete_direction(navigation_direction)