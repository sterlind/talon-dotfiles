not mode: sleep
-
# Major modes
^mouse$: user.mouse_toggle()
^mode dictate$:
    mode.disable("command")
    mode.enable("dictation")
^mode command$:
    mode.disable("dictation")
    mode.enable("command")

# Language modes
^force python$: user.code_set_language_mode("python")
^clear language mode$:
    user.code_clear_language_mode()