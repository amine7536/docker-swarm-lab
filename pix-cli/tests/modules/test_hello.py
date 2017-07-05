# -*- coding: utf-8 -*-

"""Tests for our `diva hello` subcommand."""

from subprocess import PIPE, Popen
from unittest import TestCase


class TestHello(TestCase):
    def test_returns_multiple_lines(self):
        output = Popen(['diva', 'hello'], stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_hello_world(self):
        output = Popen(['diva', 'hello'], stdout=PIPE).communicate()[0]
        self.assertTrue('Hello, world!' in output)
