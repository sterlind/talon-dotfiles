^talon restart$: user.execute_user_script_nb("restart_talon.ps1")
^fix parrot$: 
    x = user.join_paths(path.talon_user(), "parrot_integration.py")
    user.execute_user_script("touch_script.ps1", "-Path {x}")
talon open log: menu.open_log()
talon open rebel: menu.open_repl()