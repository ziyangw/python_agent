from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

def _render(request, template_name, context=None, content_type=None,
            status=None, using=None):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    print('hey!')
    content = loader.render_to_string(template_name, context, request,
                                      using=using)
    return HttpResponse(content, content_type, status)
