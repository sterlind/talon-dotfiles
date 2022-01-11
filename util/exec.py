import os
import subprocess

from talon import Module, Context, actions
from talon_init import TALON_USER

mod = Module()


def execute_user_script_inner(file: str, arg: str, handler):
    print(arg)
    script_path = os.path.join(TALON_USER, "mine", "scripts", file)
    handler(f"powershell -WindowStyle hidden {script_path} {arg}")

@mod.action_class
class Actions:
    def join_paths(left: str, right: str):
        "joins two paths together"
        return os.path.join(left, right)

    def system_command(cmd: str):
        """execute a command on the system"""
        # os.system(cmd)
        result = subprocess.run(cmd, shell=True, capture_output=True)
        print(result)

    def system_command_nb(cmd: str):
        """execute a command on the system without blocking"""
        subprocess.Popen(cmd, shell=True)
    
    def execute_user_script(file: str, arg: str = None):
        "executes a user script"
        execute_user_script_inner(file, arg, actions.user.system_command)

    def execute_user_script_nb(file: str, arg: str = None):
        "executes a user script unblocking"
        execute_user_script_inner(file, arg, actions.user.system_command_nb)
