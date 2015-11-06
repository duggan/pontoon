# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
import io
from subprocess import CalledProcessError
from pytest import raises
import pytest
from mock import MagicMock, patch


# Put lib dir into path so can be tested without installing
lib_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, lib_dir)

from docopt import docopt
from docopt import DocoptExit
from pontoon.command import Command
from pontoon import ui
from pontoon import configure
from pontoon.mocking import (_raise, capture_stdout, event_response,
                             get_builtins)


_manager = MagicMock(name='Manager')

_input = MagicMock(name='_input')


_expanduser = MagicMock(name='expanduser')


_sleep = MagicMock(name='sleep')


_call = MagicMock(name='call')


_Popen = MagicMock(name='Popen')


_open = MagicMock(name='open')


_getuid = MagicMock(name='getuid')
_getuid.return_value = 1

_fake_config = {
            'api_token': 'foobar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': 'foo'}

@patch('pontoon.ui.sleep', _sleep)
@patch('pontoon.ui.user_input', _input)
class TestUI:

    thisfile = os.path.realpath(__file__)

    def test_ticker(self):
        with capture_stdout() as capture:
            ui.ticker()
        assert capture.result == ""

    def test_ask_yesno(self):
        _input.return_value = "y"
        assert ui.ask_yesno("Foo?") is True
        _input.return_value = "n"
        assert ui.ask_yesno("Bar?") is False

    def test_ask(self):
        _input.return_value = "bar"
        assert ui.ask("Foo") == 'bar'

    def test_valid_path(self):
        assert ui.valid_path(self.thisfile)

    def test_full_path(self):
        assert ui.full_path(self.thisfile) == self.thisfile

    def test_filename_from_path(self):
        assert ui.filename_from_path(self.thisfile) == 'test_models'

    def test_mask(self):
        assert ui.mask('tiny') == '****'
        assert ui.mask('somewhatlonger') == '***********ger'
        assert (ui.mask('reallylongperhapsabighashorsomethinglikethat') ==
                ('***********************************glikethat'))

    def test_format_droplet_info(self):
        # FIXME: needs lib mocking
        pass

    def test_format_event(self):
        # FIXME: needs lib mocking
        pass

    def test_message(self):
        with capture_stdout() as capture:
            ui.message("foo bar baz")
        assert capture.result == "foo bar baz\n"

    def test_heading(self):
        heading = (
            "------------------------------------------------------------\n"
            "|                                                          |\n"
            "|                           foo                            |\n"
            "|                                                          |\n"
            "------------------------------------------------------------\n"
        )
        with capture_stdout() as capture:
            ui.heading("foo")
        assert heading.strip() == capture.result.strip()

    def test_notify(self):
        notify = (
            "************************************************************\n"
            "*                                                          *\n"
            "*                           foo                            *\n"
            "*                                                          *\n"
            "************************************************************"
        )
        with capture_stdout() as capture:
            ui.notify("foo")
        assert notify.strip() == capture.result.strip()

    def test_warning(self):
        warning = (
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            "!                                                          !\n"
            "!                           foo                            !\n"
            "!                                                          !\n"
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        )
        with capture_stdout() as capture:
            ui.warning("foo")
        assert warning.strip() == capture.result.strip()


@patch('pontoon.configure.getuid', _getuid)
@patch('pontoon.configure.expanduser', _expanduser)
@patch('pontoon.configure.call', _call)
@patch('pontoon.configure.Popen', _Popen)
@patch('%s.open' % get_builtins(), _open)
class TestConfigure:

    def test_ssh_tools(self):
        _Popen.side_effect = ["/usr/bin/ssh-keygen", "/usr/bin/openssl"]
        assert configure.ssh_tools() is True

        _Popen.side_effect = lambda *args, **kwargs: (
            _raise(CalledProcessError("foo", "bar")))
        assert configure.ssh_tools() is False

    def test_regenerate_public_key(self):
        _call.return_value = None
        assert configure.regenerate_public_key("foo", "bar") is None

    def test_rsa_keygen(self):
        _call.side_effect = lambda x: print("generating a public key" % x)
        with capture_stdout() as capture:
            configure.rsa_keygen("foo")
        assert capture.result == "generating a public key\n"

    def test_combined(self):
        fake_config = (
            "api_token: foobar\n"
            "auth_key: ~/.ssh/foo\n"
            "auth_key_name: foo"
        ).encode('UTF-8')

        _open.side_effect = lambda *args, **kwargs: io.BytesIO(fake_config)
        assert configure.combined() == {
            'api_token': 'foobar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': 'foo',
            'username': 'root',
        }

    def test_register_key(self):
        # FIXME: needs lib mocking
        pass

    def test_read_key(self):
        key_response = 'bazbazbazbazbazbazbaz'.encode('UTF-8')
        _open.side_effect = lambda *args, **kwargs: io.BytesIO(key_response)
        key = configure.read_key('/foo/bar/baz')
        assert key == 'bazbazbazbazbazbazbaz'.encode('UTF-8')

    def test_create_config(self):
        _open.side_effect = lambda *args, **kwargs: io.BytesIO()
        assert configure.create_config({'foo': 'bar', 'baz': 'boo'}) is None
        _open.side_effect = lambda *args, **kwargs: io.BytesIO()
        _getuid.return_value = 0
        assert configure.create_config({'foo': 'bar', 'baz': 'boo'}) is None

    def test_read_config(self):
        fake_config = (
            "api_token: foobar\n"
            "auth_key: ~/.ssh/foo\n"
            "auth_key_name: foo"
        ).encode('UTF-8')

        _open.side_effect = lambda *args, **kwargs: io.BytesIO(fake_config)
        assert configure.read_config() == {
            'api_token': 'foobar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': 'foo',
        }
        fake_config = (
            "api_token: foobar\n"
            "auth_key: ~/.ssh/foo\n"
        ).encode('UTF-8')

        _open.side_effect = lambda *args, **kwargs: io.BytesIO(fake_config)
        assert configure.read_config() == {
            'api_token': 'foobar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': None,
        }
        _open.side_effect = lambda x: (_raise(IOError))
        configure.read_config() == {
            'api_token': 'foobar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': None,
        }


class TestCommand:

    def test_command(self):
        doc = """Usage: command foo"""
        config = _fake_config

        with raises(DocoptExit):
            args = docopt(str(doc))

        class SmallCommand(Command):

            def __init__(self, config, args):
                self.config = config
                self.args = args
                self.manager = _manager(token=config['api_token'])

            def foo(self):
                print("foo-answer")

            def bar(self):
                print("bar-answer")

        with capture_stdout() as capture:
            output = SmallCommand(config, docopt(str(doc), argv=['foo'])).run()
        assert capture.result == "foo-answer\n"

        with capture_stdout() as capture:
            output = SmallCommand(config, []).run("bar")
        assert capture.result == "bar-answer\n"
