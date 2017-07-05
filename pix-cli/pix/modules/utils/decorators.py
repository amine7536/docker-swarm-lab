# -*- coding: utf-8 -*-

from functools import wraps


def register_action(method_or_name):
    """Adds a `module_method` attribute to methods decorated, giving the method a
    module method name (this is used by the ModuleMetaclass to register this
    method as a supported method. This provides an explicit way to add
    new Module subclasses with varying methods, without remembering to
    configure things along the way."""

    def decorator(method):
        if callable(method_or_name):
            method.module_method = method.__name__
        else:
            method.module_method = method_or_name

        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper

    if callable(method_or_name):
        return decorator(method_or_name)

    return decorator
