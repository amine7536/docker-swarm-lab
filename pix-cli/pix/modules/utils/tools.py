import os
import errno
import json
from jinja2 import Environment, FileSystemLoader
from colors import Color
from logger import logger
from ..base import ModuleConfigError


"""
Collection of useful functions
"""


def render_template(template_folder, template_file, app_settings):
    """
    Renders Nginx configuration
    :param template_folder: folder with templates
    :param template_file: template filename
    :param app_settings: application settings from json file
    :return: rendered template
    """
    j2_env = Environment(loader=FileSystemLoader(template_folder), trim_blocks=True)

    return j2_env.get_template(template_file).render(
        app_settings=app_settings
    )


def write_file(filename, content):
    """
    Write nginx confugration file in /etc/nginx
    :param filename: file name
    :param conf: render conf
    :return:
    """
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

    try:
        file_handle = os.open(filename, flags)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Failed as the file already exists.
            logger.error("File %s already exists" % filename)
            raise SystemExit("Exception %s" % e)
        else:
            # Something unexpected went wrong so re-raise the exception.
            raise SystemExit("Exception %s" % e)
    else:
        # No exception, so the file must have been created successfully.
        with os.fdopen(file_handle, 'w') as file_obj:
            file_obj.write(content)
    return True


def make_dir(directory_name):
    try:
        os.makedirs(directory_name)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(directory_name):
            pass
        else:
            # Something unexpected went wrong so re-raise the exception.
            raise SystemExit("Exception %s" % e)
    return os.path.dirname(directory_name)

def create_sym_link(src, dst):
    """
    Create symlink
    :param src:
    :param dst:
    :return:
    """
    try:
        os.symlink(src, dst)
    except OSError as e:
        if e.errno == errno.EEXIST:
            logger.error("Symlink %s already exists" % dst)
            raise SystemExit("Exception %s" % e)
        else:
            # Something unexpected went wrong so re-raise the exception.
            raise SystemExit("Exception %s" % e)
    return True


def read_json_file(json_file):
    """
    Reads Json from file
    :param json_file:
    :return:
    """
    try:
        parsed_json = json.loads(open(json_file).read())
    except Exception as e:
        logger.error("Unable to read configuration file %s" % json_file)
        raise SystemExit("Exception: %s" % e)
    return parsed_json


def user_input(prompt, validate):
    """
    Prompts user for input until response is not empty
    :param prompt:
    :param validate:
    :return:
    """

    while True:
        try:
            answer = raw_input(prompt)
            if validate(answer): break
        except ValueError as e:
            print e

    return answer


def user_confirm(prompt=None, resp=False):
    """
    Prompts for yes or no response from the user. Returns True for yes and
    False for no.
    """

    colored = Color().colored

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        try:
            answer = raw_input(colored(prompt, color='yellow'))
            if not answer:
                return resp
            if answer not in ['y', 'Y', 'n', 'N']:
                print 'please enter y or n.'
                continue
            if answer == 'y' or answer == 'Y':
                return True
            if answer == 'n' or answer == 'N':
                return False
        except ValueError as e:
            print e


def validate_params(settings, required_settings):
    """
    Check params
    :param settings:
    :param required_settings:
    :return:
    """
    for s in required_settings:
        if s in settings:
            if not settings[s]:
                raise ModuleConfigError('Missing configuration parameter %s' % s)
            pass
        else:
            raise ModuleConfigError('Missing configuration parameter %s' % s)