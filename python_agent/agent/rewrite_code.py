import __builtin__
from ast import *
import compileall
import sys
import itertools


class RewriteCode(NodeTransformer):

    def __init__(self, filename):
        self.filename = filename
        self.enter_linenos = {}
        self.reach_linenos = {}
        self.counter = itertools.count()

    def visit_Module(self, module_node):
        body_future = []
        body_rest = []
        for node in module_node.body:
            node = self.visit(node)
            if (not body_rest and isinstance(node, ImportFrom) and
                node.module == "__future__"):
                body_future.append(node)
            else:
                body_rest.append(node)

        import_line = parse("from python_agent.ast_import import *").body[0]
        register_line = parse(
            "ast_enter, ast_leave, ast_reached = register_module(%r, %r, %r)" %
            (self.filename, self.enter_linenos, self.reach_linenos)).body[0]

        lineno = 1
        if body_future:
            lineno = body_future[0].lineno
        for new_node in (import_line, register_line):
            new_node.col_offset = 1
            new_node.lineno = lineno

        new_body = body_future + [import_line, register_line] + body_rest
        return Module(body=new_body)

    def visit_Str(self, node):
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        if isinstance(node.value, Str):
            new_node = parse("str_assign('%s')" % node.value.s).body[0]
            if_node = If(test=Num(n=1), body=[node, new_node], orelse=[])
            copy_location(if_node, node)
            fix_missing_locations(if_node)
            return if_node
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, Name) and node.func.id == "str":
            new_node = Call(func=Name(id='str_function_call', ctx=Load()),
                            args=node.args, keywords=[], staratgs=None,
                            kwargs=None)
            copy_location(new_node, node)
            fix_missing_locations(new_node)
            return new_node
        return node


old_compile = __builtin__.compile


def compile(source, filename, mode, flags=0):
    if flags == PyCF_ONLY_AST:
        return old_compile(source, filename, mode, flags)
    assert(mode == "exec")
    code = open(filename).read()
    tree = parse(code, filename)
    tree = RewriteCode(filename).visit(tree)
    code = old_compile(tree, filename, "exec")
    return code

__builtin__.compile = compile

exit_status = int(not compileall.main())
sys.exit(exit_status)