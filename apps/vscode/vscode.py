from talon import Context, Module

ctx = Context()
mod = Module()
mod.apps.vscode = """
os: windows
and app.name: Visual Studio Code
os: windows
and app.exe: Code.exe
"""

ctx.matches = r"""
app: vscode
"""