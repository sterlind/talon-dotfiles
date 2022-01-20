tag: user.scoped_navigation
-

list this <user.text>: user.scoped_navigation("list", "default", "", text)
scout this <user.text>: user.scoped_navigation("find", "default", "", text)
scout all <user.text>: user.scoped_navigation("find", "default", "all", text)
pop this <user.text>: user.scoped_navigation("go", "default", "", text)

list {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("list", navigation_scope, "", text or "")
scout {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("find", navigation_scope, "", text or "")
scout all {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("find", navigation_scope, "all", text or "")
pop {user.navigation_scope} [<user.text>] [over]:
    user.scoped_navigation("go", navigation_scope, "", text or "")