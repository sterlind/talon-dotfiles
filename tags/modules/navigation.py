from talon import Module

mod = Module()
mod.tag("navigation")

@mod.action_class
class UserActions:
    def go_back():
        """Navigate back to previous location"""
    def go_forward():
        """Navigate forwards to next location"""