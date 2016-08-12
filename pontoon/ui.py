# -*- coding: utf-8 -*-

from __future__ import print_function

# Windows / missing-readline compat
try:
    import readline
except ImportError:
    pass

import socket
import yaml
import textwrap
from os.path import (isfile, expanduser,
                     basename, splitext, join)
from time import sleep
from sys import stdout

# Python 2.6 compatibility
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

# Python 2/3 compatibility
try:
    user_input = raw_input
except NameError:
    user_input = input


# Borrowed from http://stackoverflow.com/questions/5121931
def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def ticker():
    """A loading/waiting indicator.

    Sends a '.' to the screen, resets, and sleeps.
    """
    stdout.write('.')
    stdout.flush()
    sleep(1)


def ask_yesno(question):
    """Present a string as a yes/no question on an interactive prompt"""
    question = "%s (y/n)" % question
    if user_input("%-15s: " % question).strip().lower() == 'y':
        return True
    return False


def ask(question):
    """Present a question with freeform input on an interactive prompt"""
    question += ':'
    response = user_input("%-15s " % question)
    return response


def valid_path(path):
    """Check whether a given string resolves to a path on the filesystem"""
    return isfile(expanduser(path))


def full_path(path):
    """Expand a ~/ prefixed path to a full path"""
    return join(expanduser(path))


def filename_from_path(path):
    """Get a filename from a given path"""
    return splitext(basename(expanduser(path)))[0]


def machine():
    try:
        return socket.gethostname()
    except OSError:
        return "pontoon"


def mask(text, masker='*'):
    """Hide part of a string,

    If the input is small, hide the entire string.
    Otherwise, show only the last few characters.
    """
    length = len(text)
    coverage = length / 100.0 * 20
    if (coverage < 0.9):
        result = (masker * length)
        return result
    masked_length = int(length - coverage)
    result = "%s%s" % ((masker * masked_length), text[masked_length:])
    return result


def format_droplet_info(machine):
    """Present Droplet information in a more human parseable format"""

    d = OrderedDict()
    d['id'] = machine.id
    d['size'] = machine.size_slug
    d['image'] = machine.image['slug']
    d['region'] = machine.region['slug']
    d['ip_address'] = machine.ip_address
    d['status'] = machine.status

    # Fields we want to remove / replace
    redacted = ['token', 'end_point', 'image', 'region',
                'size', 'mock_data', 'mock_status', 'mocked']
    details = machine.__dict__.copy()
    for k, v in machine.__dict__.items():
        if k.startswith('_') or k in redacted:
            del details[k]

    for k, v in details.items():
        d[k] = v
    return d


def format_event(action):
    """Present event information in a more human parseable format"""
    e = OrderedDict()
    e['id'] = action.id
    e['type'] = action.type
    e['resource_type'] = action.resource_type
    e['started_at'] = action.started_at
    e['completed_at'] = action.completed_at

    redacted = ['token', 'end_point', 'region',
                'mock_data', 'mock_status', 'mocked']
    details = action.__dict__.copy()
    for k, v in action.__dict__.items():
        if k.startswith('_') or k in redacted:
            del details[k]

    for k, v in details.items():
        e[k] = v

    return e


def format_item(item):
    """Present any item in more human parseable format"""
    i = OrderedDict()
    i['id'] = item.id
    i['name'] = item.name

    redacted = ['token', 'end_point',
                'mock_data', 'mock_status', 'mocked']
    details = item.__dict__.copy()
    for k, v in item.__dict__.items():
        if k.startswith('_') or k in redacted:
            del details[k]

    for k, v in details.items():
        i[k] = v

    return i


def message(text):
    """Wrapper for the `print` function"""
    print(text)
    return text


def yaml_message(data):
    """ Formats output as ordered YAML """
    message(ordered_dump(data,
                         Dumper=yaml.SafeDumper,
                         default_flow_style=False))


def heading(text, boxwidth=60):
    """Create a 'heading' styled textbox"""
    return box(text, decor="-", decor_y="|", boxwidth=boxwidth)


def notify(text, boxwidth=60):
    """Create a 'notification' styled textbox"""
    return box(text, decor="*", boxwidth=boxwidth)


def warning(text, boxwidth=60):
    """Create a 'warning' styled textbox"""
    return box(text, decor="!", boxwidth=boxwidth)


def line(length=60, decor='-'):
    """Write a line"""
    print(decor * length)


def box(text, decor='*', decor_x=None, decor_y=None,
        boxwidth=60, borderwidth=2):
    """Create a formatted textbox for highlighting important information"""
    decor_x = decor_x if decor_x else decor
    decor_y = decor_y if decor_y else decor
    decor_x_width = len(decor_x) if len(decor_x) > 0 else 1
    decor_y_width = len(decor_y) if len(decor_y) > 0 else 1
    decor_x_multiplier = int(boxwidth / decor_x_width)
    decor_y_multiplier = decor_y_width * 2

    textwidth = boxwidth - decor_y_multiplier - (borderwidth * 2)
    text = textwrap.wrap(text, textwidth)
    text = "\n".join([
        "{decor_y}{text}{decor_y}".format(
            decor_y=decor_y, text=m.center(
                boxwidth - decor_y_multiplier)) for m in text])
    border_x = (decor_x * decor_x_multiplier)
    border_space = "{decor_y}{spacer}{decor_y}".format(
        decor_y=decor_y, spacer=(" " * (boxwidth - decor_y_multiplier)))
    spacing = (' ' * boxwidth)
    text = "\n".join([
        spacing, border_x, border_space, text,
        border_space, border_x, spacing])
    print(text)
    return text
