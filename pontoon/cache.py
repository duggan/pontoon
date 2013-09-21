# -*- coding: utf-8 -*-

"""
Taken from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
"""

import logging
import functools

logger = logging.getLogger(__name__)


def cache(obj):
    """Cache the given object hashed on arguments"""
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        logline = (obj.__module__, obj.__name__, args)
        if key not in cache:
            logger.debug("caching %s.%s %s" % logline)
            cache[key] = obj(*args, **kwargs)
        logger.debug("returning cached %s.%s %s" % logline)
        return cache[key]
    return memoizer
