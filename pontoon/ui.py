# -*- coding: utf-8 -*-

from __future__ import print_function

import readline
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
except:
    user_input = input


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


def format_droplet_info(machine, size="", region="", image=""):
    """Present Droplet information in a more human parseable format"""
    d = OrderedDict()
    d['id'] = machine.id
    d['name'] = machine.name
    d['size'] = size
    d['image'] = image
    d['region'] = region

    del machine.region_id
    del machine.image_id
    del machine.size_id

    for k, v in machine.__dict__.items():
        d[k] = v

    return d


def format_event(event, type="", droplet=""):
    """Present event information in a more human parseable format"""
    e = OrderedDict()
    e['id'] = event.id
    e['type'] = type
    e['droplet'] = droplet

    del event.event_type_id
    del event.droplet_id

    for k, v in event.__dict__.items():
        e[k] = v

    return e


def message(text):
    """Wrapper for the `print` function"""
    print(text)
    return text


def heading(text, boxwidth=60):
    """Create a 'heading' styled textbox"""
    return box(text, decor="-", decor_y="|", boxwidth=boxwidth)


def notify(text, boxwidth=60):
    """Create a 'notification' styled textbox"""
    return box(text, decor="*", boxwidth=boxwidth)


def warning(text, boxwidth=60):
    """Create a 'warning' styled textbox"""
    return box(text, decor="!", boxwidth=boxwidth)


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
                boxwidth-decor_y_multiplier)) for m in text])
    border_x = (decor_x * decor_x_multiplier)
    border_space = "{decor_y}{spacer}{decor_y}".format(
        decor_y=decor_y, spacer=(" " * (boxwidth-decor_y_multiplier)))
    spacing = (' ' * boxwidth)
    text = "\n".join([
        spacing, border_x, border_space, text,
        border_space, border_x, spacing])
    print(text)
    return text
