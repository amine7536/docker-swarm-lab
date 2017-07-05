# -*- coding: utf-8 -*-

"""
Usage:
    pix-cli <module> [options] [<svc_name>] [<attributes>...]

Options:
    -h --help               Show this screen.
    -v                      Show Debug
    --version               Show version.
    --branch=<svc_branch>    Service Branch

Examples:
    pix-cli services:build MySvcName --branch my-feature

Help:
    For help using this tool, please open an issue on the Github repository:
    https://github.com/amine7536/pixelfactory-cli
"""

import re
from inspect import getmembers, isclass
from docopt import docopt
from pix.modules.utils import logger, setup_logger
from . import __version__


def main():
    """
    Main CLI
    """
    import modules
    arguments = docopt(__doc__, version=__version__)
    module = arguments.get('<module>')
    verbose = arguments.get('-v')

    setup_logger(verbose)
    action = 'help'

    r = re.compile('.*:.*')
    if r.match(module) is not None:
        (module, action) = module.split(':')

    if not action:
        """ if not action set dispatch help action"""
        action = 'help'


    if hasattr(modules, module) and action:
        """ Look for the right module """
        module = getattr(modules, module)
        commands = getmembers(module, isclass)
        command = [command[1] for command in commands if command[0] != 'Base'][0]
        command = command(arguments)

        try:
            command.dispatch(action)
        except Exception as e:
            logger.error("Main => %s" % e)
