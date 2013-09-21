# -*- coding: utf-8 -*-

import re
import sys
import contextlib
from random import randrange
from datetime import datetime, timedelta

from .exceptions import ClientException

# Python 2/3 compatibility for capture_stdout
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class Data(object):
    pass


def timestamp(hours=0):
    """Mocked Digital Ocean timestamp"""
    return (datetime.utcnow() + timedelta(
        hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_builtins():
    """Python 2.x and 3.x have different names for accessing builtins"""
    try:
        __import__('builtins')
        return 'builtins'
    except ImportError:
        return '__builtin__'


def _raise(ex=None):
    """Wrapper for exceptions so they can be thrown from inside lambdas"""
    if ex:
        exception.append(ex)
    if len(exception):
        raise exception.pop()


def event_response():
    return {
        'event_id': randrange(9999),
        'status': 'OK',
    }


@contextlib.contextmanager
def capture_stdout():
    """Captures STDOUT and turns it into an object"""
    old = sys.stdout
    capturer = StringIO()
    sys.stdout = capturer
    data = Data()
    yield data
    sys.stdout = old
    data.result = capturer.getvalue()


exception = []

mocked = {
    'droplets': [
        {
            'id': 1, 'name': 'foo', 'image_id': 1, 'region_id': 2,
            'backups_active': False, 'status': 'active',
            'ip_address': '192.0.2.1', 'size_id': 3, 'locked': False,
            'created_at': timestamp(-200), 'private_ip_address': None,
        },
        {
            'id': 2, 'name': 'bar', 'image_id': 1, 'region_id': 2,
            'backups_active': False, 'status': 'active',
            'ip_address': '192.0.2.2', 'size_id': 2, 'locked': False,
            'created_at': timestamp(-5), 'private_ip_address': None,
        },
        {
            'id': 3, 'name': 'baz', 'image_id': 1, 'region_id': 1,
            'backups_active': False, 'status': 'active',
            'ip_address': '192.0.2.3', 'size_id': 1, 'locked': False,
            'created_at': timestamp(), 'private_ip_address': None,
        },
    ],
    'regions': [
        {
            'id': 1, 'name': 'Foo York 1',
        },
        {
            'id': 2, 'name': 'Bardam 1',
        },
        {
            'id': 3, 'name': 'Foo Barbaz 1',
        },
        {
            'id': 4, 'name': 'Foo York 2',
        },
    ],
    'images': [
        {
            'id': 1, 'name': 'Foobuntu 12.04 x64', 'distribution': 'Foobuntu',
        },
        {
            'id': 2, 'name': 'Foobuntu 12.04 x32', 'distribution': 'Foobuntu',
        },
        {
            'id': 3, 'name': 'Bar 6.0 x64', 'distribution': 'Bar',
        },
        {
            'id': 4, 'name': 'Bar 6.0 x32', 'distribution': 'Bar',
        },
    ],
    'snapshots': [
        {
            'id': 1024, 'name': 'snapshot-foo',
            'distribution': 'Foobuntu',
        },
        {
            'id': 2048, 'name': 'snapshot-bar-2013-10-10',
            'distribution': 'Foobuntu',
        },
        {
            'id': 4096, 'name': 'snapshot-baz-pre-install',
            'distribution': 'Foobuntu',
        },
    ],
    'sizes': [
        {
            'id': 1, 'name': '512MB',
        },
        {
            'id': 2, 'name': '1GB',
        },
        {
            'id': 3, 'name': '2GB',
        },
    ],
    'ssh_keys': [
        {
            'id': 1, 'name': 'foobarbaz',
            'ssh_pub_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEA1on8gxCGJJWSRT'
                           '4uOrR13mUaUk0hRf4RzxSZ1zRbYYFw8pfGesIFoEuVth4HKyF8'
                           'k1y4mRUnYHP1XNMNMJl1JcEArC2asV8sHf6zSPVffozZ5TT4Sf'
                           'sUu/iKy9lUcCfXzwre4WWZSXXcPff+EHtWshahu3WzBdnGxm5X'
                           'oi89zcE= test@example.com'
        },
    ],
    'events': [
        {
            'id': 999, 'action_status': 'done', 'droplet_id': 1,
            'event_type_id': 1, 'percentage': 100,
        },
        {
            'id': 888, 'action_status': 'done', 'droplet_id': 2,
            'event_type_id': 2, 'percentage': 100,
        },
        {
            'id': 777, 'action_status': 'done', 'droplet_id': 3,
            'event_type_id': 3, 'percentage': 100,
        },
    ],
}


def _respond_denied(target, method='GET', params={}):
    """Fake 403 denied response from Digital Ocean"""
    raise ClientException("Mock Access Denied")


def _respond(target, method='GET', params={}):
    """Fake out responses from Digital Ocean."""

    if len(params) > 0:
        if re.match("^/images$", target):
            if 'filter' in params:
                return {'images': (mocked.get('snapshots') +
                                   mocked.get('images'))}

        if re.match("^/images/\d+/transfer$", target):
            if 'region_id' in params:
                return event_response()

        elif re.match("^/droplets/\d+/resize$", target):
            if 'size_id' in params:
                return event_response()

        elif re.match("^/droplets/\d+/snapshot$", target):
            if 'name' in params:
                return event_response()

        elif re.match("^/droplets/\d+/rebuild$", target):
            if 'image_id' in params:
                return event_response()

        elif re.match("^/droplets/\d+/rename$", target):
            if 'name' in params:
                return event_response()

        elif re.match("^/droplets/\d+/restore$", target):
            if 'image_id' in params:
                return event_response()

        elif re.match("^/droplets/new$", target):
            new = {
                'id': randrange(100, 999),
                'name': params['name'],
                'image_id': params['image_id'],
                'region_id': params['region_id'],
                'backups_active': False,
                'status': 'new',
                'ip_address': '192.0.2.%s' % randrange(10, 255),
                'size_id': params['size_id'],
                'locked': False,
                'created_at': timestamp(),
                'private_ip_address': None
                }
            mocked['droplets'].append(new)

            return {'droplet': new}

        elif re.match("^/ssh_keys/new$", target):
            new = {
                'id': randrange(100, 999),
                'name': params['name'],
                'ssh_pub_key': params['ssh_pub_key']
                }
            mocked['ssh_keys'].append(new)

            return {'ssh_key': new}

        elif re.match("^/ssh_keys/\d+/edit$", target):
            r = re.match("^/ssh_keys/(\d+)/edit$", target)
            id = int(r.group(1))
            replaced = []
            new = {
                'id': id,
                'ssh_pub_key': params['ssh_pub_key']
            }
            for key in mocked.get('ssh_keys'):
                if key['id'] == id:
                    new['name'] = key['name']
                    replaced.append(new)
                else:
                    replaced.append(key)
            mocked['ssh_keys'] = replaced

            return {'ssh_key': next((
                k for k in mocked.get(
                    'ssh_keys') if k['id'] == id), None)}

        elif re.match("^/droplets/\d+/destroy$", target):
            if 'scrub_data' in params:
                return event_response()
    else:
        options = {
            '/droplets': {'droplets': mocked.get('droplets')},
            '/regions': {'regions': mocked.get('regions')},
            '/images': {'images': (mocked.get('images') +
                                   mocked.get('snapshots'))},
            '/sizes': {'sizes': mocked.get('sizes')},
            '/ssh_keys': {'ssh_keys': mocked.get('ssh_keys')},
            '/droplets/\d+/reboot': event_response(),
            '/droplets/(\d+)': lambda x: {'droplet': next(
                (d for d in mocked.get('droplets') if d['id'] == x), None)},
            '/droplets/\d+/power_cycle': event_response(),
            '/droplets/\d+/power_off': event_response(),
            '/droplets/\d+/power_on': event_response(),
            '/droplets/\d+/enable_backups': event_response(),
            '/droplets/\d+/disable_backups': event_response(),
            '/droplets/\d+/shutdown': event_response(),
            '/droplets/\d+/password_reset': event_response(),
            '/images/(\d+)': lambda x: {'image': next(
                (d for d in (mocked.get('images') +
                             mocked.get('snapshots')) if d['id'] == x), None)},
            '/images/\d+/destroy': {'event': event_response()},
            '/events/(\d+)': lambda x: {'event': next(
                (d for d in mocked.get('events') if d['id'] == x), None)},
            '/ssh_keys/(\d+)': lambda x: {'ssh_key': next(
                (d for d in mocked.get('ssh_keys') if d['id'] == x), None)},
            '/ssh_keys/\d+/destroy': event_response(),

        }
        for pattern, func in options.items():
            r = re.match("^%s$" % pattern, target)
            if r:
                try:
                    arg = r.group(1)
                    res = func(int(arg))
                    if not next(iter(res.values())):
                        raise ClientException("A Mock Error")
                    return res
                except IndexError:
                    pass
                return func
