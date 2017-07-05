# -*- coding: utf-8 -*-

from json import dumps
from .base import Module
from .utils.decorators import register_action


class Hello(Module):
    """
    Hello Module
    """

    @register_action('help')
    def module_help(self):
        print """Hello Module
        Actions : world, run
        Options:
            --name=<name> [Default: John ]
        """

    @register_action('world')
    def my_funtion(self):
        name = self.options.get('--name')
        print 'Hello, %s\n' % name
        print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)

    @register_action('run')
    def my_other_functio(self):
        name = self.options.get('--name')
        print 'Goodbye, %s\n' % name
        print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)
