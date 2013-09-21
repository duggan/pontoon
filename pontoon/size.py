# -*- coding: utf-8 -*-

from .exceptions import ClientException, SizeException
from . import debug, cache


class Size:
    """Manage operations related to Droplet size"""

    def __init__(self, render):
        self.render = render

    @cache
    @debug
    def list(self):
        """List Droplet sizes"""
        try:
            return [s for s in self.render('sizes', '/sizes')]
        except ClientException as e:
            raise SizeException(str(e))

    @cache
    @debug
    def id_from_name(self, name):
        """Tranlsate size name into ID"""
        name = name.upper()
        matches = [s.id for s in self.list() if s.name == name]
        if len(matches) == 1:
            return matches[0]
        else:
            raise SizeException('"%s" is not a valid size' % name)

    @cache
    @debug
    def name_from_id(self, id):
        """Translate size ID into human readable value"""
        ret = next((s.name for s in self.list() if s.id == id), None)
        if ret:
            return ret
        raise SizeException("No size found for id %s" % id)
