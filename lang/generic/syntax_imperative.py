from talon import Module
from typing import Union

mod = Module()
mod.tag("imperative_language")

@mod.action_class
class UserActions:
    def code_statement_variable_assign(name: Union[str, list[str]], value: str = None):
        """Inserts a variable assignment"""

    def code_statement_return_nothing():
        """Inserts a empty return statement"""

    def code_statement_return(expression: str = None):
        """Inserts a return statement"""
        
    def code_block_if(expression: str = None):
        """Inserts an if block"""

    def code_block_while(expression: str = None):
        """Inserts a while loop"""

    def code_block_for(name: str = None, expression: str = None):
        """Inserts a for loop"""

    def code_block_try_catch():
        """Insert a try-catch block"""

    def code_block_scope(name: str, value: str = None):
        """Inserts a variable scope block"""