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

from docopt import DocoptExit
from pontoon import (PontoonException, DropletException,
                     SnapshotException, ConfigureException,
                     SSHKeyException, ImageException,
                     RegionException, SizeException,
                     EventException)
from pontoon import Pontoon
from pontoon import Command
from pontoon import ClientException
from pontoon.pontoon import Struct
from pontoon import ui
from pontoon import configure
from pontoon.mocking import (_raise, capture_stdout, event_response,
                             get_builtins, _respond, mocked)


_request = MagicMock(name='request')
_request.side_effect = _respond


class Data(object):
    pass


_input = MagicMock(name='_input')


_expanduser = MagicMock(name='expanduser')


_sleep = MagicMock(name='sleep')


_call = MagicMock(name='call')


_Popen = MagicMock(name='Popen')


_open = MagicMock(name='open')


_getuid = MagicMock(name='getuid')
_getuid.return_value = 1


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestRender:

    client = Pontoon('foo', 'bar')

    def test_render(self):
        with raises(ClientException):
            self.client.render('foo', "/foo/%s/bar" % Struct)

        with raises(ClientException):
            self.client.render('foo', '/foo/100/bar')


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestDroplet(object):

    droplet = Pontoon('foo', 'bar').droplet

    def test_list(self):
        _request.side_effect = _respond
        for server in self.droplet.list():
            assert isinstance(server, Struct)

    def test_id_from_name(self):
        _request.side_effect = _respond

        assert self.droplet.id_from_name('foo') == 1

        with raises(DropletException):
            self.droplet.id_from_name('not-a-droplet')

        mocked['droplets'].append({
            'id': 9,
            'name': 'baz',
        })
        with raises(DropletException):
            self.droplet.id_from_name('baz')

    def test_name_from_id(self):
        _request.side_effect = _respond
        assert self.droplet.name_from_id(2) == 'bar'

        with raises(DropletException):
            self.droplet.name_from_id(999)

    def test_show(self):
        _request.side_effect = _respond

        server = self.droplet.show("foo")
        assert server.id == 1
        server = self.droplet.show("baz")
        assert server.id == 3
        server = self.droplet.show("bar")
        assert server.id == 2

        with raises(DropletException):
            self.droplet.show(200)

    def test_create(self):
        _request.side_effect = _respond
        result = self.droplet.create(name="newfoo", size="512MB",
                                     image="Bar 6.0 x64", region="Bardam 1",
                                     keys=["foobarbaz"])
        assert result.size_id == 1
        assert result.image_id == 3
        assert result.region_id == 2

        with raises(DropletException):
            result = self.droplet.create(name="newfoo", size="512MB",
                                         image="Bar 6.0 x64",
                                         region="Bardam 1",
                                         keys=["foobarbaz"])

        with raises(DropletException):
            self.droplet.create()

    def test_start(self):
        _request.side_effect = _respond
        e = self.droplet.start('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.start('non-existant')

    def test_shutdown(self):
        _request.side_effect = _respond
        e = self.droplet.shutdown('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.shutdown('non-existant')

    def test_snapshot(self):
        _request.side_effect = _respond
        e = self.droplet.snapshot('foo', 'snapshot-foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.snapshot('non-existant', 'snapshot-foo')

    def test_restore(self):
        _request.side_effect = _respond
        e = self.droplet.restore('foo', 'snapshot-foo')
        assert isinstance(e, int)

        with raises(SnapshotException):
            self.droplet.restore('foo', 'not-snapshot')

    def test_rebuild(self):
        _request.side_effect = _respond
        e = self.droplet.rebuild('foo', 'Foobuntu 12.04 x64')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.rebuild('non-existant', 'not-snapshot')

        with raises(ImageException):
            self.droplet.rebuild('foo', 'not-snapshot')

    def test_rename(self):
        _request.side_effect = _respond
        e = self.droplet.rename('foo', 'foofoo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.rename('foo', 'bar')

    def test_resize(self):
        _request.side_effect = _respond
        e = self.droplet.resize('foo', '1GB')
        assert isinstance(e, int)

        with raises(SizeException):
            self.droplet.resize('foo', '64MB')

    def test_destroy(self):
        _request.side_effect = _respond
        e = self.droplet.destroy('foo')
        assert isinstance(e, int)
        e = self.droplet.destroy('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.destroy('non-existant')

    def test_status(self):
        _request.side_effect = _respond
        status = self.droplet.status('foo')
        assert status == 'active'

        with raises(DropletException):
            self.droplet.status('non-existant')

    def test_reboot(self):
        _request.side_effect = _respond
        e = self.droplet.reboot('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.reboot('non-existant')

    def test_powercycle(self):
        _request.side_effect = _respond
        e = self.droplet.powercycle('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.powercycle('non-existant')

    def test_poweroff(self):
        _request.side_effect = _respond
        e = self.droplet.poweroff('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.poweroff('non-existant')

    def test_backups(self):
        _request.side_effect = _respond
        e = self.droplet.backups('enable', 'foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.backups('enable', 'non-existant')

        e = self.droplet.backups('disable', 'foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.backups('disable', 'non-existant')

    def test_passwordreset(self):
        _request.side_effect = _respond
        e = self.droplet.passwordreset('foo')
        assert isinstance(e, int)

        with raises(DropletException):
            self.droplet.passwordreset('non-existant')


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestImage(object):

    image = Pontoon('foo', 'bar').image

    def test_list(self):
        for img in self.image.list():
            assert isinstance(img, Struct)

    def test_show(self):
        img = self.image.show("Foobuntu 12.04 x64")
        assert img.id == 1

    def test_oses(self):
        assert sorted(['Bar', 'Foobuntu']) == sorted(self.image.oses())

    def test_id_from_name(self):
        assert 1 == self.image.id_from_name('Foobuntu 12.04 x64')
        with raises(ImageException):
            foo = self.image.id_from_name('Foo')

    def test_name_from_id(self):
        assert 'Foobuntu 12.04 x32' == self.image.name_from_id(2)
        with raises(ImageException):
            foo = self.image.name_from_id(10)


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestSnapshot(object):

    snapshot = Pontoon('foo', 'bar').snapshot
    snapshot_list = MagicMock('snapshot_list')
    some_snapshot = Data()
    some_snapshot.id = 2
    some_snapshot.name = 'snapshot-bar'
    snapshot_list.return_value = [some_snapshot, some_snapshot]

    def test_list(self):
        for snap in self.snapshot.list():
            assert isinstance(snap, Struct)

    def test_show(self):
        img = self.snapshot.show("snapshot-foo")
        assert img.id == 1024

    def test_id_from_name(self):
        assert 1024 == self.snapshot.id_from_name('snapshot-foo')
        with raises(SnapshotException):
            foo = self.snapshot.id_from_name('not-a-snapshot')

    @patch('pontoon.snapshot.Snapshot.list', snapshot_list)
    def test_id_from_name_two(self):
        with raises(SnapshotException):
            foo = self.snapshot.id_from_name('snapshot-bar')

    def test_destroy(self):
        e = self.snapshot.destroy('snapshot-foo')
        assert e.status == 'OK'
        with raises(SnapshotException):
            foo = self.snapshot.destroy('not-a-snapshot')

    def test_transfer(self):
        e = self.snapshot.transfer('snapshot-foo', 'Bardam 1')
        assert isinstance(e, int)


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestEvent(object):

    event = Pontoon('foo', 'bar').event

    def test_show(self):
        e = self.event.show(999)
        assert e.action_status == 'done'

        with raises(EventException):
            e = self.event.show(444)

    def test_type_from_id(self):
        t = self.event.type_from_id(8)
        assert t == 'snapshot'

        t = self.event.type_from_id(10)
        assert t == 'unknown (10)'


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestSize(object):

    size = Pontoon('foo', 'bar').size

    def test_list(self):
        for s in self.size.list():
            assert isinstance(s, Struct)

    def test_id_from_name(self):
        assert 1 == self.size.id_from_name('512MB')
        with raises(SizeException):
            self.size.id_from_name('Nonexistant')

    def test_name_from_id(self):
        assert '2GB' == self.size.name_from_id(3)
        with raises(SizeException):
            self.size.name_from_id(99)


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestRegion(object):

    region = Pontoon('foo', 'bar').region

    def test_list(self):
        for r in self.region.list():
            assert isinstance(r, Struct)

    def test_id_from_name(self):
        assert 1 == self.region.id_from_name('Foo York 1')
        with raises(RegionException):
            self.region.id_from_name('Nonexistant')

    def test_name_from_id(self):
        assert 'Bardam 1' == self.region.name_from_id(2)
        with raises(RegionException):
            self.region.name_from_id(99)


@patch('pontoon.pontoon.Pontoon.request', _request)
class TestSSHKey(object):

    sshkey = Pontoon('foo', 'bar').sshkey

    def test_list(self):
        for s in self.sshkey.list():
            assert isinstance(s, Struct)

    def test_show(self):
        key = self.sshkey.show("foobarbaz")
        assert key.name == 'foobarbaz'

    def test_add(self):
        key = self.sshkey.add("barbaz",
                              "this_is_a_poor_attempt_at_ssh_public_key")
        assert key.name == 'barbaz'

        with raises(SSHKeyException):
            key = self.sshkey.add("foobarbaz",
                                  "this_is_a_poor_attempt_at_ssh_public_key")

    def test_replace(self):
        key = self.sshkey.replace("foobarbaz",
                                  "this_is_a_poor_attempt_at_ssh_public_key")
        assert key.name == 'foobarbaz'

    def test_destroy(self):
        e = self.sshkey.destroy("foobarbaz")
        assert e == 'OK'

    def test_id_from_name(self):
        assert 1 == self.sshkey.id_from_name('foobarbaz')
        with raises(SSHKeyException):
            self.sshkey.id_from_name('Nonexistant')

    def test_name_from_id(self):
        assert 'foobarbaz' == self.sshkey.name_from_id(1)
        with raises(SSHKeyException):
            self.sshkey.name_from_id(99)


@patch('pontoon.pontoon.Pontoon.request', _request)
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
        pontoon = Pontoon('foo', 'bar')
        resp = ui.format_droplet_info(pontoon.droplet.show('foo'),
                                      size="512MB", region="Bardam 1",
                                      image="Foobuntu 12.04 x64")
        assert resp['id'] == 1
        assert resp['name'] == 'foo'
        assert resp['region'] == 'Bardam 1'

    def test_format_event(self):
        pontoon = Pontoon('foo', 'bar')
        resp = ui.format_event(pontoon.event.show(999),
                               type=8,
                               droplet='foo')
        assert resp['id'] == 999
        assert resp['type'] == 8
        assert resp['droplet'] == 'foo'

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
@patch('pontoon.pontoon.Pontoon.request', _request)
class TestConfigure:

    def test_ssh_tools(self):
        _Popen.side_effect = ["/usr/bin/ssh-keygen", "/usr/bin/openssl"]
        assert configure.ssh_tools() is True

        _Popen.side_effect = lambda cmd, stdout: (
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
            "client_id: foo\n"
            "api_key: bar\n"
            "auth_key: ~/.ssh/foo\n"
            "auth_key_name: foo"
        ).encode('UTF-8')

        _open.side_effect = lambda *args, **kwargs: io.BytesIO(fake_config)
        assert configure.combined() == {
            'client_id': 'foo',
            'api_key': 'bar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': 'foo',
            'username': 'root',
            'scrub_data': True,

        }

    def test_list_keys(self):
        r = configure.list_keys({'client_id': 'foo', 'api_key': 'bar'})
        assert 'foobarbaz' in [k.name for k in r]

    def test_register_key(self):
        r = configure.register_key({'client_id': 'foo', 'api_key': 'bar'},
                                   'bar',
                                   'bazbazbazbazbazbazbaz')
        assert r is None

        with raises(ConfigureException):
            configure.register_key({'client_id': 'foo', 'api_key': 'bar'},
                                   'foobarbaz',
                                   'bazbazbazbazbazbazbaz')

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
            "client_id: foo\n"
            "api_key: bar\n"
            "auth_key: ~/.ssh/foo\n"
            "auth_key_name: foo"
        ).encode('UTF-8')

        _open.side_effect = lambda *args, **kwargs: io.BytesIO(fake_config)
        assert configure.read_config() == {
            'client_id': 'foo',
            'api_key': 'bar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': 'foo',
        }
        fake_config = (
            "client_id: foo\n"
            "api_key: bar\n"
            "auth_key: ~/.ssh/foo\n"
        ).encode('UTF-8')

        _open.side_effect = lambda *args, **kwargs: io.BytesIO(fake_config)
        assert configure.read_config() == {
            'client_id': 'foo',
            'api_key': 'bar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': None,
        }
        _open.side_effect = lambda x: (_raise(IOError))
        configure.read_config() == {
            'client_id': 'foo',
            'api_key': 'bar',
            'auth_key': '~/.ssh/foo',
            'auth_key_name': None,
        }


class TestCommand:

    def test_command(self):
        doc = """Usage: command foo"""
        argv = ['foo']

        class SmallCommand(Command):

            def foo(self):
                print("foo-answer")

            def bar(self):
                print("bar-answer")

        command = SmallCommand(doc, argv=argv)

        with capture_stdout() as capture:
            output = command.run()
        assert capture.result == "foo-answer\n"

        with capture_stdout() as capture:
            output = command.run("bar")
        assert capture.result == "bar-answer\n"

        with raises(DocoptExit):
            command = SmallCommand(doc, argv=['baz'])
