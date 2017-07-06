import sys
import inspect


def count_loaded_class():
    count = 0
    for obj in sys.modules.values():
        if obj is not None:
            try:
                count += len(inspect.getmembers(obj, inspect.isclass))
            except:
                pass
    return count
