from collections import defaultdict
import traceback
import atexit
import linecache

loaded_modules = []
STR_FUNCTION_CALL_COUNTER = 0
STR_ASSIGN_COUNTER = 0


class FileInfo(object):
    def __init__(self, filename, enter_linenos, reach_linenos):
        self.filename = filename
        self.enter_linenos = enter_linenos
        self.reach_linenos = reach_linenos
        self.ast_enter = defaultdict(int)
        self.ast_leave = defaultdict(int)
        self.ast_reach = defaultdict(int)


def register_module(filename, enter_linenos, reach_linenos):
    info = FileInfo(filename, enter_linenos, reach_linenos)
    loaded_modules.append(info)
    return info.ast_enter, info.ast_leave, info.ast_reach


def str_function_call(args):
    try:
        global STR_FUNCTION_CALL_COUNTER
        STR_FUNCTION_CALL_COUNTER += 1
        print("str function call #%d, with value %s" % (STR_FUNCTION_CALL_COUNTER, str(args)))
        return str(args)
    except Exception, e:
        print("Could not call str: %s" % e)
        raise


def str_assign(value):
    global STR_ASSIGN_COUNTER
    STR_ASSIGN_COUNTER += 1
    print("str assign #%d, with value %s" % (STR_ASSIGN_COUNTER, str(value)))
