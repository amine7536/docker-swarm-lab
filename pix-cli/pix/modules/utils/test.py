import re
from tools import user_input, user_confirm

# def validate(answer):
#     if answer:
#         return True
#     else:
#         raise ValueError('Empty')

# def validate(port):
#     if port.isdigit():
#         return True
#     else:
#         raise ValueError('Application Port must be numbers only')


def validate(url):
    r = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if r.match(url) is not None:
        return True
    else:
        raise ValueError('Invalid url: %s' % url)



user_input('Hello ', validate)
