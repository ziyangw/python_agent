from urlparse import parse_qs
from webob import Request, Response
from agent import *
from helpers import *
from memory_profiler import memory_usage
from ..ast_import import *
import time
import uuid
import sys
import inspect
import cProfile


class RequestAnalysis(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print("------Request Start------")
        ast_request_start()
        start = time.time()
        request = Request(environ)
        request.accept += 'text/html'
        request.make_body_seekable()
        parsed_request = parse_qs(request.body)
        request_environ = locals()
        request_mem_usage = memory_usage()
        agent.profile = cProfile.Profile()
        agent.profile.enable()

        def response_analysis(status, headers, exc_info=None):
            ast_response_start()
            response_environ = locals()
            # print("---------------")
            request = Request(environ)
            request.accept += 'text/html'
            request.make_body_seekable()
            parsed_request = parse_qs(request.body)
            # print(request)
            # print(parsed_request)
            # print("String objects from request that are garbage collected: ")
            # RequestAnalysis.compute_diff(request_environ, response_environ)
            # print("String objects created between request and response: ")
            # RequestAnalysis.compute_diff(response_environ, request_environ)
            # print("---------------")
            # print("String objects created: %d" % (STR_FUNCTION_CALL_COUNTER+STR_ASSIGN_COUNTER))
            str.called = 0
            response_id = str(uuid.uuid4())
            agent.response_holder.add(
                response_id, {'request_environ': environ, 'status': status,
                              'headers': headers})

            response_cls = inspect.getmembers(sys.modules[__name__], inspect.isclass)
            print("Response ID assigned: %s" % response_id)
            end = time.time()
            total_time = end - start
            print("Total time taken: %s" % total_time)
            agent.file.write("Time: %s \n" % str(total_time))
            response_mem_usage = memory_usage()
            mem_used = response_mem_usage[0] - request_mem_usage[0]
            print('Memory used: %s' % str(mem_used))
            agent.memory_logger.write("Mem Used: %s \n" % str(mem_used))
            # print("------Request End------")
            agent.profile.disable()
            # print('Class loaded: %d' % count_loaded_class())
            # pstats.Stats(agent.profile).sort_stats("filename").print_stats()
            # print(pstats.Stats(agent.profile).strip_dirs().sort_stats("calls").__dict__)
            print("------Request End------")
            response = Response()
            response.body = request.body
            # return response(environ, start_response)
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
        if not hasattr(diff, '__iter__') or type(diff) in [list, tuple, str,
                                                           file]:
            print(key, diff)
        else:
            try:
                for key in diff:
                    RequestAnalysis.iterate_print(key, diff[key])
            except:
                print(key, diff)
