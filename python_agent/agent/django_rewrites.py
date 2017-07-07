from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.http.cookie import SimpleCookie


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
