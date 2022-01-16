from talon import Module, actions, ctrl

from talon_plugins import eye_mouse
from talon_plugins.eye_mouse import config, toggle_control

mod = Module()
mod.mode("mouse")

@mod.action_class
class Actions:
    def mouse_disable():
        """Disable the mouse mode"""
        toggle_control(False)
        actions.mode.disable("user.mouse")

    def mouse_toggle():
        "Toggle mouse mode"
        enabled = not config.control_mouse
        toggle_control(enabled)
        if enabled:
            actions.mode.enable("user.mouse")
        else:
            actions.mode.disable("user.mouse")

    def mouse_drag_toggle():
        "Toggle mouse drag"
        if 0 in ctrl.mouse_buttons_down():
            ctrl.mouse_click(button=0, up=True)
        else:
            ctrl.mouse_click(button=0, down=True)

    def mouse_calibrate():
        """Start calibration"""
        eye_mouse.calib_start()