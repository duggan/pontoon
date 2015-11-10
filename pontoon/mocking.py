# -*- coding: utf-8 -*-

import re
import sys
import contextlib
from random import randrange
from datetime import datetime, timedelta

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
    exception = []
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
