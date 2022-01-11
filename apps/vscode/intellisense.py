from talon import actions, fs, app
import os
import csv
import re
class Intellisense:
    def __init__(self):
        app.register("ready", self.on_ready)
    
    def on_ready(self):
        pass