tag: user.scoped_navigation
-

list {user.navigation_scope} <user.text> [over]: user.scoped_list(navigation_scope, text)
scout {user.navigation_scope} <user.text> [over]: user.scoped_find(navigation_scope, text)
scout all {user.navigation_scope} <user.text> [over]: user.scoped_find_all(navigation_scope, text)
pop {user.navigation_scope} <user.text> [over]: user.scoped_go(navigation_scope, text)