import imp
import sys
from types import ModuleType
from django_rewrites import _render
from django_rewrites import httpResponse__init__
from django_rewrites import __call__


class DummyModule(ModuleType):
    def __getattr__(self, key):
        return None

    __all__ = []  # support wildcard imports


class ImportHooks(object):
    def __init__(self, *args):
        self.module_names = args

    def find_module(self, fullname, path=None):
        try:
            if fullname in self.module_names:
                self.path = path
                return self
            return None
        except:
            return DummyModule(fullname)

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        if name == "django.shortcuts":
            name = 'shortcuts'
            module_info = imp.find_module(name, self.path)
            module = imp.load_module(name, *module_info)
            module.render = _render

        elif name == "django.http":
            name = 'http'
            module_info = imp.find_module(name, self.path)
            module = imp.load_module(name, *module_info)
            module.HttpResponseBase.init = httpResponse__init__

        elif name == "django.core.handlers.wsgi":
            name = 'wsgi'
            once = False
            module_info = imp.find_module(name, self.path)
            module = imp.load_module(name, *module_info)
            module.WSGIHandler.__call__ = __call__
            sys.modules["django.core.handlers.wsgi"] = module

            return sys.modules["django.core.handlers.wsgi"]
        else:
            module_info = imp.find_module(name, self.path)
            module = imp.load_module(name, *module_info)
            sys.modules[name] = module
        return module


sys.meta_path.append(ImportHooks('django.shortcuts', 'django.http',
                                 'django.core.handlers.wsgi'))
