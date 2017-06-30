from urlparse import parse_qs
from webob import Request


class RequestAnalysis(object):

    def __init__(self, app):
        self.app = app

    """
    def __call__(self, environ, start_response):
        try:
            content = werkzeug.wsgi.get_input_stream(environ)
            request_body = content.read()
        except Exception, e:
            print(str(e))
            request_body = "0"
        d = parse_qs(request_body)
        print(environ.get('QUERY_STRING'))
        print("this is parsed body %s" % d)

        return self.app(environ, start_response)
    """

    def __call__(self, environ, start_response):
        request = Request(environ)
        request.make_body_seekable()
        parsed_request = parse_qs(request.body)
        print(parsed_request)
        return self.app(environ, start_response)
