from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.http.cookie import SimpleCookie
from django.urls import set_script_prefix
from django.core import signals
from django.utils import six
import re
from django.utils.encoding import (
    force_str, force_text, repercent_broken_unicode,
)

ISO_8859_1, UTF_8 = str('iso-8859-1'), str('utf-8')
_slashes_re = re.compile(br'/+')


def _render(request, template_name, context=None, content_type=None,
            status=None, using=None):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    print('We just hacked your render function lol')
    content = loader.render_to_string(template_name, context, request,
                                      using=using)
    return HttpResponse(content, content_type, status, context)


def httpResponse__init__(self, content_type=None, status=None, reason=None,
                         charset=None, context=None):
    # _headers is a mapping of the lower-case name to the original case of
    # the header (required for working with legacy systems) and the header
    # value. Both the name of the header and its value are ASCII strings.
    self._headers = {}
    self._closable_objects = []
    # This parameter is set by the handler. It's necessary to preserve the
    # historical behavior of request_finished.
    self._handler_class = None
    self.cookies = SimpleCookie()
    self.closed = False
    self.context = None
    if status is not None:
        try:
            self.status_code = int(status)
        except (ValueError, TypeError):
            raise TypeError('HTTP status code must be an integer.')

        if not 100 <= self.status_code <= 599:
            raise ValueError(
                'HTTP status code must be an integer from 100 to 599.')
    self._reason_phrase = reason
    self._charset = charset
    if content_type is None:
        content_type = '%s; charset=%s' % (settings.DEFAULT_CONTENT_TYPE,
                                           self.charset)
    self['Content-Type'] = content_type


def get_bytes_from_wsgi(environ, key, default):
    """
    Get a value from the WSGI environ dictionary as bytes.

    key and default should be str objects. Under Python 2 they may also be
    unicode objects provided they only contain ASCII characters.
    """
    value = environ.get(str(key), str(default))
    # Under Python 3, non-ASCII values in the WSGI environ are arbitrarily
    # decoded with ISO-8859-1. This is wrong for Django websites where UTF-8
    # is the default. Re-encode to recover the original bytestring.
    return value.encode(ISO_8859_1) if six.PY3 else value


def get_script_name(environ):
    """
    Returns the equivalent of the HTTP request's SCRIPT_NAME environment
    variable. If Apache mod_rewrite has been used, returns what would have been
    the script name prior to any rewriting (so it's the script name as seen
    from the client's perspective), unless the FORCE_SCRIPT_NAME setting is
    set (to anything).
    """
    if settings.FORCE_SCRIPT_NAME is not None:
        return force_text(settings.FORCE_SCRIPT_NAME)

    # If Apache's mod_rewrite had a whack at the URL, Apache set either
    # SCRIPT_URL or REDIRECT_URL to the full resource URL before applying any
    # rewrites. Unfortunately not every Web server (lighttpd!) passes this
    # information through all the time, so FORCE_SCRIPT_NAME, above, is still
    # needed.
    script_url = get_bytes_from_wsgi(environ, 'SCRIPT_URL', '')
    if not script_url:
        script_url = get_bytes_from_wsgi(environ, 'REDIRECT_URL', '')

    if script_url:
        if b'//' in script_url:
            # mod_wsgi squashes multiple successive slashes in PATH_INFO,
            # do the same with script_url before manipulating paths (#17133).
            script_url = _slashes_re.sub(b'/', script_url)
        path_info = get_bytes_from_wsgi(environ, 'PATH_INFO', '')
        script_name = script_url[:-len(path_info)] if path_info else script_url
    else:
        script_name = get_bytes_from_wsgi(environ, 'SCRIPT_NAME', '')

    return script_name.decode(UTF_8)


def __call__(self, environ, start_response):
    set_script_prefix(get_script_name(environ))
    signals.request_started.send(sender=self.__class__, environ=environ)
    request = self.request_class(environ)
    response = self.get_response(request)
    try:
        environ['my_template'] = response.content
    except:
        environ['my_template'] = ""
    response._handler_class = self.__class__

    status = '%d %s' % (response.status_code, response.reason_phrase)
    response_headers = [(str(k), str(v)) for k, v in response.items()]
    for c in response.cookies.values():
        response_headers.append((str('Set-Cookie'), str(c.output(header=''))))
    start_response(force_str(status), response_headers)
    if getattr(response, 'file_to_stream', None) is not None and environ.get(
            'wsgi.file_wrapper'):
        response = environ['wsgi.file_wrapper'](response.file_to_stream)
    return response
