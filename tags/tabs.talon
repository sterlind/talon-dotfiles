tag: user.tabs
-

tab last:                   app.tab_previous()
tab last <number_small>:
    app.tab_previous()
    repeat(number_small - 1)
tab next:                   app.tab_next()
tab next <number_small>:
    app.tab_next()
    repeat(number_small - 1)
tab <number_small>:         user.tab_jump(number_small)
tab minus <number_small>:   user.tab_jump_from_back(number_small)
tab final:                  user.tab_final()
tab back:                   user.tab_back()
tab left:                   user.tab_move_left()
tab right:                  user.tab_move_right()
tab new:                    app.tab_open()
tab duplicate:              user.tab_duplicate()
tab (reopen | restore):     app.tab_reopen()

tab close:                  app.tab_close()
tab close others:           user.tab_close_others()
tab close all:              user.tab_close_all()
tab close left:             user.tab_close_left()
tab close right:            user.tab_close_right()
tab last close:
    app.tab_previous()
    sleep(50ms)
    app.tab_close()
tab next close:
    app.tab_next()
    sleep(50ms)
    app.tab_close()
tab <number_small> close:
    user.tab_jump(number_small)
    sleep(50ms)
    app.tab_close()
tab final close:
    user.tab_final()
    sleep(50ms)
    app.tab_close()