# -*- coding: utf-8 -*-

from __future__ import with_statement

__all__ = ['Module', 'ModuleError', 'ModuleRuntimeError', 'ModuleConfigError']

class ModuleMeta(type):
    """The purpose of this metaclass is to allow sub-classes to register methods
    using a decorator: `register_action(action_name)`, then use
    `module.supports_action(action_name)` to check at runtime if the module
    supports a given action.

    This metaclass adds a `supported_methods` attribute to sub-classes, which
    is a dicitonary of method lookups. The methods added to this dictionary are
    ones decorated with `register_action('action_name')`. The method
    name passed into the decorator is used for the dictionary key. If no method
    name is passed to the decorator, the method is mapped in the dictionary with
    its real name.

    @register_action('start')
    def start_and_log(self, app, **kwargs):
        ... implementation details omitted.

    """
    def __new__(cls, name, bases, dct):
        dct['supported_methods'] = {}
        for member in dct.itervalues():
            if hasattr(member, 'module_method'):
                dct['supported_methods'][getattr(member, 'module_method')] = member
        return type.__new__(cls, name, bases, dct)


class Module(object):
    """
    Base Module Class
    """
    __metaclass__ = ModuleMeta

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def supports_method(self, method_name):
        """Returns True or False, depending on whether the method_name passed in
        represents the name of a registered method for the module class
        in question.

        Example:

        module = SomeModule(args)
        if module.supports_method('create_app'):
            module_response = module.dispatch('create_app', myapp)
            if module_response.success:
                return 'Oh Yeah!'
        """
        return method_name in self.supported_methods

    def dispatch(self, method_name, *args, **kwargs):
        """Call a module method with its registered name. This method does not
        have to be used. You can optionally call a method directly.

        Inside ExampleModule class:

        @register_action('create_app')
        def create_app_with_options(self, options)
            # Do some stuff
            return

        Usage:

        app_module = ExampleModule()
        ExampleModule.dispatch('create_app', options)
        """
        try:
            module_method = self.supported_methods[method_name]
        except KeyError:
            raise ModuleRuntimeError('Method {0} not supported by {1}'.format(
                method_name, self.__class__.__name__))
        else:
            return module_method(self, *args, **kwargs)


class ModuleError(Exception):
    pass


class ModuleConfigError(ModuleError):
    pass


class ModuleRuntimeError(ModuleError):
    pass
