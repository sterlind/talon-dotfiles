from talon import Module, actions

mod = Module()
mod.tag("git")

@mod.action_class
class UserActions:
    def git_status():
        """Git status command"""
        
    def git_commit():
        """Git commit command"""
        
    def git_push():
        """Git push command"""
        
    def git_pull():
        """Git pull command"""