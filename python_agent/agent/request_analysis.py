from urlparse import parse_qs
from webob import Request
from response_holder import ResponseHolder
import time
import uuid

class Agent(object):

    def __init__(self):
        def counting(fn):
            def wrapper(*args, **kwargs):
                wrapper.called += 1
                return fn(*args, **kwargs)
            wrapper.called = 0
            wrapper.__name__ = fn.__name__
            return wrapper
        global str
        str = counting(str)
        str.__init__ = counting(str.__init__)
        str.__new__ = counting(str.__new__)
        self.response_holder = ResponseHolder()

global agent
agent = Agent()
file = open("testfile.txt","w")


class RequestAnalysis(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start = time.time()
        request = Request(environ)
        request.make_body_seekable()
        parsed_request = parse_qs(request.body)
        request_environ = locals()

        def response_analysis(status, headers, exc_info=None):
            response_environ = locals()
            # print("---------------")
            # print("String objects from request that are garbage collected: ")
            # RequestAnalysis.compute_diff(request_environ, response_environ)
            # print("String objects created between request and response: ")
            # RequestAnalysis.compute_diff(response_environ, request_environ)
            # print("---------------")
            print("String objects created: %d" % str.called)
            str.called = 0
            response_id = str(uuid.uuid4())
            agent.response_holder.add(
                response_id, {'request_environ': environ, 'status': status, 'headers': headers})
            print("Response ID assigned: %s" % response_id)
            return start_response(status, headers, exc_info)

        end = time.time()
        total_time = end - start
        file.write(str(total_time))
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
