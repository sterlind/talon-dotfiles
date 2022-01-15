mode: user.mouse
-

run calibration: user.mouse_calibrate()

parrot(barred_lambda): mouse_click(0)
parrot(glottal_q): mouse_click(1)
parrot(kiss_click): user.mouse_drag_toggle()

touch: mouse_click(0)
righty: mouse_click(1)
<user.key_modifiers> touch: 
	key("{key_modifiers}:down")
	mouse_click(0)
	key("{key_modifiers}:up")
<user.key_modifiers> righty: 
	key("{key_modifiers}:down")
	mouse_click(1)
	key("{key_modifiers}:up")