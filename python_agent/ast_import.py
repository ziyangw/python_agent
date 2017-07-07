from collections import defaultdict
import traceback
import atexit
import linecache
import inspect
import types

loaded_modules = []
STR_FUNCTION_CALL_COUNTER = 0
STR_ASSIGN_COUNTER = 0
CLASS_LOADED_COUNT = 0


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


def ast_request_start():
    global STR_FUNCTION_CALL_COUNTER, STR_ASSIGN_COUNTER
    STR_FUNCTION_CALL_COUNTER = STR_ASSIGN_COUNTER = 0


def ast_response_start():
    global STR_FUNCTION_CALL_COUNTER, STR_ASSIGN_COUNTER
    print("String objects created: %d" % (STR_FUNCTION_CALL_COUNTER+STR_ASSIGN_COUNTER))
    return STR_FUNCTION_CALL_COUNTER+STR_ASSIGN_COUNTER


def ast_class_load():
    global CLASS_LOADED_COUNT
    return CLASS_LOADED_COUNT


def str_function_call(args):
    try:
        global STR_FUNCTION_CALL_COUNTER
        STR_FUNCTION_CALL_COUNTER += 1
        print("str function call #%d, with value %s" % (STR_FUNCTION_CALL_COUNTER, str(args)))
        return str(args)
    except Exception, e:
        print("Could not call str: %s" % e)
        raise


def str_interpolate(left, right):
    print("string interpolation %s with %s" % (left, right))
    return left % right


def str_assign(value):
    global STR_ASSIGN_COUNTER
    STR_ASSIGN_COUNTER += 1
    print("str assign #%d, with value %s" % (STR_ASSIGN_COUNTER, str(value)))


def isclass(name):
    return isinstance(name, (types.TypeType, types.ClassType))


def import_name(name, alias):
    global CLASS_LOADED_COUNT
    CLASS_LOADED_COUNT += 1
    if len(alias) == 0:
        print("Class #%d %s loaded" % (CLASS_LOADED_COUNT, name))
    elif len(alias) > 0:
        print("Class #%d %s loaded as %s" % (CLASS_LOADED_COUNT, name, alias))


def fromimport_name(module, name, alias):
    global CLASS_LOADED_COUNT
    CLASS_LOADED_COUNT += 1
    if len(alias) == 0:
        print("Class #%d %s loaded" % (CLASS_LOADED_COUNT, name))
    elif len(alias) > 0:
        print("Class #%d %s loaded as %s" % (CLASS_LOADED_COUNT, name, alias))
