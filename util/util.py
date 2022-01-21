from talon import Module
from collections.abc import Iterable

mod = Module()

def merge(*args) -> dict:
    """Merge dictionaries and lists"""
    result = {}
    for arg in args:
        if isinstance(arg, dict):
            for k, v in arg.items():
                if v == None:
                    del result[k]
                else:
                    result[k] = v
        elif isinstance(arg, Iterable):
            for v in arg:
                result[v] = v
        else:
            raise Exception("Unknown type " + str(type(arg)))
    return result

@mod.action_class
class Actions:
    def cycle(value: int, min: int, max: int) -> int:
        """Cycle value between minimum and maximum"""
        if value < min:
            return max
        if value > max:
            return min
        return value

    def cramp(value: int, min: int, max: int) -> int:
        """Cramp value between minimum and maximum"""
        if value < min:
            return min
        if value > max:
            return max
        return value
