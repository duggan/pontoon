# -*- coding: utf-8 -*-

from .exceptions import ClientException, ImageException
from . import debug, cache


class Image:
    """Manage operations related to images."""

    def __init__(self, render):
        self.render = render

    @cache
    @debug
    def list(self):
        """List available images."""
        try:
            return [s for s in self.render('images', '/images')]
        except ClientException as e:
            raise ImageException(str(e))

    def show(self, name):
        """Show details for a single image."""
        id = self.id_from_name(name)
        try:
            return self.render('image', '/images/%s' % id)
        except ClientException as e:
            raise ImageException(str(e))

    @debug
    def oses(self):
        """Return a list of the Operating System flavours made availble
        through the various images."""
        oses = []
        for image in self.list():
            oses.append(image.distribution)
        return [i for i in set(oses)]

    @cache
    @debug
    def id_from_name(self, name):
        """Translate image name into an ID"""
        res = next((
            r.id for r in self.list() if r.name.lower() == name.lower()),
            None)
        if res:
            return res
        raise ImageException("No image called %s" % name)

    @cache
    @debug
    def name_from_id(self, id):
        """Translate image ID into a name"""
        try:
            res = self.render('image', '/images/%s' % id).name
            if res:
                return res
        except ClientException:
            pass
        raise ImageException("No image found for id %s" % id)
