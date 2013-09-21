# -*- coding: utf-8 -*-

from .exceptions import ClientException, RegionException
from . import debug, cache


class Region:
    """Manage operations related to regions."""

    def __init__(self, render):
        self.render = render

    @cache
    @debug
    def list(self):
        """List regions"""
        try:
            return [s for s in self.render('regions', '/regions')]
        except ClientException as e:
            raise RegionException(str(e))

    @cache
    @debug
    def id_from_name(self, name):
        """Translate region name into ID"""
        ret = next((
            r.id for r in self.list() if r.name.lower() == name.lower()),
            None)
        if ret:
            return ret
        raise RegionException("No region called %s" % name)

    @cache
    @debug
    def name_from_id(self, id):
        """Translate region ID into name"""
        ret = next((r.name for r in self.list() if r.id == id), None)
        if ret:
            return ret
        raise RegionException("No region with id %s" % id)
