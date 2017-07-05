# -*- coding: utf-8 -*-


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from pix import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=pix', '--cov-report=term-missing'])
        raise SystemExit(errno)

requirements = [
    'docopt',
    'pymongo'
]

test_requirements = [
    # test requirements here
]

setup(
    name='pix',
    version=__version__,
    description='A command line program in Python.',
    long_description=long_description,
    url='https://github.com/amine7536/pixelfactory-cli',
    author='Amine Benseddik',
    author_email='amine.benseddik@gmail.com',
    license='BSD',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=requirements,
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov','Sphinx'],
    },
    entry_points={
        'console_scripts': [
            'pix=pix.main:main',
        ],
    },
    tests_require=test_requirements,
    cmdclass={'test': RunTests},
)
