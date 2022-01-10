from talon import Module, actions

from talon_plugins import eye_mouse
from talon_plugins.eye_mouse import config, toggle_control

mod = Module()
mod.mode("mouse")

@mod.action_class
class Actions:
    def mouse_toggle():
        "Toggle mouse mode"
        enabled = not config.control_mouse
        toggle_control(enabled)
        if enabled:
            actions.mode.enable("user.mouse")
        else:
            actions.mode.disable("user.mouse")
    def mouse_calibrate():
        """Start calibration"""
        eye_mouse.calib_start()