from django.utils.functional import curry


def patch_class(class_or_instance, method_name, wrapper_function,
                external_replacement_function=None):
    original_function = getattr(class_or_instance, method_name)

    if callable(external_replacement_function) or hasattr(
            external_replacement_function, '__call__'):

        setattr(class_or_instance, method_name,
                curry(wrapper_function, external_replacement_function,
                      original_function))
    else:
        raise AttributeError("No attribute __call__ found in %s" % method_name)


def patch(class_or_instance, method_name, new_function=None):
    def wrapper_with_patch(external_patch_function, original_function,
                           *args, **kwargs):
        return external_patch_function(original_function, *args, **kwargs)

    return patch_class(class_or_instance, method_name, wrapper_with_patch,
                       new_function)
