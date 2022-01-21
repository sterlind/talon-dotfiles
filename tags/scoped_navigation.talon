tag: user.scoped_navigation
-

list this [<user.text>]: user.scoped_navigation("list", "default", "", text or "")
scout this [<user.text>]: user.scoped_navigation("find", "default", "", text or "")
scout all [<user.text>]: user.scoped_navigation("find", "default", "all", text or "")
pop this <user.text>: user.scoped_navigation("go", "default", "", text)

list [{user.navigation_scope}] that:
    text = edit.selected_text()
    user.scoped_navigation("list", navigation_scope or "default", "", text or "")

scout [{user.navigation_scope}] that:
    text = edit.selected_text()
    user.scoped_navigation("find", navigation_scope or "default", "", text or "")

scout all [{user.navigation_scope}] that:
    text = edit.selected_text()
    user.scoped_navigation("find", navigation_scope or "default", "all", text or "")

pop [{user.navigation_scope}] that:
    text = edit.selected_text()
    user.scoped_navigation("go", navigation_scope or "default", "", text or "")

list {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("list", navigation_scope, "", text or "")
scout {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("find", navigation_scope, "", text or "")
scout all {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("find", navigation_scope, "all", text or "")
pop {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("go", navigation_scope, "", text or "")

list dock <user.filename> [over]:
    user.scoped_navigation("list", "document", "", filename)
scout dock <user.filename> [over]:
    user.scoped_navigation("find", "document", "", filename)
scout all dock <user.filename> [over]:
    user.scoped_navigation("find", "document", "all", filename)
pop dock <user.filename> [over]:
    user.scoped_navigation("go", "document", "", filename)