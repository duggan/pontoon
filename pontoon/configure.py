# -*- coding: utf-8 -*-

import os
import logging
import sys
from os.path import expanduser

try:
    from os import getuid
except ImportError:
    getuid = None

from subprocess import call, Popen, PIPE, CalledProcessError
from . import debug
from .exceptions import ConfigureException
from .lib import Manager, SSHKey
from . import MOCK

user_cfg = os.path.join(os.path.expanduser('~'), '.pontoon')

if sys.platform != "win32":
    sys_cfg = '/etc/pontoon.conf'
else:
    sys_cfg = ""

local_cfg = os.path.join(os.getcwd(), '.pontoon')
debug_mode = True if os.environ.get("DEBUG") else False
logformat = '%(asctime)s [%(name)s:%(levelname)s] %(message)s'
config_format = {
    'api_token': "",
    'auth_key': "",
    'auth_key_name': "",
}

defaults = {}
defaults['username'] = {
    'value': 'root',
    'title': 'Droplet login username',
}


def logger():
    """Prepare interface to logging."""
    logger = logging.getLogger('pontoon')
    formatter = logging.Formatter(logformat)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG if debug_mode else False)
    logger.addHandler(handler)
    return logger


@debug
def ssh_tools():
    """Checks for existance of SSH tools required for creating keys."""
    try:
        ssh_keygen = Popen(['command', '-v', 'ssh-keygen'],
                           stdout=PIPE, shell=True)
        openssl = Popen(['command', '-v', 'openssl'],
                        stdout=PIPE, shell=True)
        if ssh_keygen and openssl:
            return True
    except CalledProcessError:
        pass
    return False


@debug
def regenerate_public_key(private_key, public_key):
    """Generate an SSH public key from an existing private key."""
    private_key = expanduser(private_key)
    public_key = expanduser(public_key)
    openssl_keygen = ['openssl', 'rsa', '-in', private_key,
                      '-pubout', '>', public_key]
    call(openssl_keygen)


@debug
def rsa_keygen(private_key):
    """Create a new SSH key"""
    private_key = expanduser(private_key)
    rsa_keygen = ['ssh-keygen', '-t', 'rsa', '-N', '', '-f', private_key]
    call(rsa_keygen)


@debug
def combined():
    """Merge configuration defaults with values from config file."""
    config = {}
    for k, v in defaults.items():
        config[k] = v['value']
    for k, v in read_config().items():
        config[k] = v

    if MOCK:
        return {"api_token": "fake-token"}

    return config


@debug
def register_key(credentials, name, public_key):
    """Register an SSH key with Digital Ocean"""
    try:
        sshkey = SSHKey(token=credentials['api_token'], mocked=MOCK)
        if not sshkey.load_by_pub_key(public_key):
            sshkey.name = name
            sshkey.public_key = public_key
            sshkey.create()
    except Exception as e:
        raise ConfigureException(str(e))


def images(credentials):
    """Retrieve image options"""
    try:
        manager = Manager(token=credentials['api_token'], mocked=MOCK)
        return manager.get_global_images()
    except Exception as e:
        raise ConfigureException(str(e))


def sizes(credentials):
    """Retrieve size options"""
    try:
        manager = Manager(token=credentials['api_token'], mocked=MOCK)
        return manager.get_all_sizes()
    except Exception as e:
        raise ConfigureException(str(e))


def regions(credentials):
    """Retrieve region options"""
    try:
        manager = Manager(token=credentials['api_token'], mocked=MOCK)
        return manager.get_all_regions()
    except Exception as e:
        raise ConfigureException(str(e))


@debug
def read_key(path):
    """Read a public SSH key from the filesystem"""
    path = expanduser(path)
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError as e:
        raise ConfigureException(str(e))


@debug
def create_config(data):
    """Create a YAML config file from a dictionary"""
    import yaml
    data = yaml.dump(data, default_flow_style=False)

    if sys.platform != "win32":
        if getuid() == 0:  # root
            loc = sys_cfg
        else:
            loc = user_cfg
    else:
        loc = user_cfg

    with open(loc, 'wb') as f:
        f.write(data.encode('UTF-8'))


@debug
def read_config():
    """Read a YAML formatted config into a dictionary"""
    import yaml
    config = config_format

    # sys_cfg empty in windows, but shouldnt affect this
    for loc in [local_cfg, user_cfg, sys_cfg]:
        try:
            with open(loc) as source:
                raw_config = source.read()
                if raw_config:
                    config = yaml.load(raw_config)
                    for expected in list(config_format.keys()):
                        if expected not in config:
                            config[expected] = None
                    return config
        except (TypeError, IOError, AttributeError):
            pass

    return config
