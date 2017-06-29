
class RequestAnalysis(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(environ.get('REQUEST_METHOD'))
        print(environ.get('PATH_INFO'))
        print(environ.get('QUERY_STRING'))

        def demo_start_response(status, headers, exc_info=None):
            print(status)
            headers.append(('DEMO', "DEMO"))
            return start_response(status, headers, exc_info)

        return self.app(environ, demo_start_response)

