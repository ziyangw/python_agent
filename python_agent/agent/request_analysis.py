from urlparse import parse_qs
from webob import Request
import os


def agent_init():
    def counting(fn):
        def wrapper(*args, **kwargs):
            wrapper.called += 1
            print(wrapper.called)
            return fn(*args, **kwargs)
        wrapper.called = 0
        wrapper.__name__ = fn.__name__
        return wrapper
    global str
    str = counting(str)
    str.__new__ = counting(str.__new__)
    str.__init__ = counting(str.__init__)

global agent_init
agent_init()

class RequestAnalysis(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        request.make_body_seekable()
        parsed_request = parse_qs(request.body)
        request_environ = locals()

        def response_analysis(status, headers, exc_info=None):
            response_environ = locals()
            print("---------------")
            print("String objects from request that are garbage collected: ")
            # RequestAnalysis.compute_diff(request_environ, response_environ)
            print("String objects created between request and response: ")
            # RequestAnalysis.compute_diff(response_environ, request_environ)
            print("---------------")
            str.called = 0
            return start_response(status, headers, exc_info)

        return self.app(environ, response_analysis)

    @staticmethod
    def compute_diff(dict1, dict2):
        key1 = set(dict1.keys())
        key2 = set(dict2.keys())
        diff = key1.difference(key2)
        diff_dict = {key: dict1[key] for key in diff}
        RequestAnalysis.iterate_print(diff, diff_dict)

    @staticmethod
    def iterate_print(key, diff):
        if not hasattr(diff, '__iter__') or type(diff) in [list, tuple, str, file]:
            print(key, diff)
        else:
            try:
                for key in diff:
                    RequestAnalysis.iterate_print(key, diff[key])
            except:
                print(key, diff)
