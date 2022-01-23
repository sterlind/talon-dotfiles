# Utility functions for language implementation

def insert_placeholders(*args):
    result = []
    count = 0
    for arg in args:
        if arg:
            result.append(arg)
        else:
            count += 1
            result.append(f"${count}")
    return tuple(result) if len(result) > 1 else result[0]