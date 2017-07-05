# -*- coding: utf-8 -*-

"""Tests for our main diva CLI module."""

from subprocess import PIPE, Popen
from unittest import TestCase

from diva import __version__


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = Popen(['diva', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = Popen(['diva', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = Popen(['diva', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), __version__)
