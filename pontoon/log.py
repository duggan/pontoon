# -*- coding: utf-8 -*-

import logging
import functools


def debug(obj):
    logger = logging.getLogger(obj.__module__)

    @functools.wraps(obj)
    def log(*args, **kwargs):
        key = str(args) + str(kwargs)
        logger.debug("%s: %s" % (obj.__name__, key))
        return obj(*args, **kwargs)
    return log
