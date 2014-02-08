# -*- coding: utf-8 -*-

from .exceptions import ClientException, SnapshotException
from . import debug, cache
from .region import Region


class Snapshot:
    """Manage operations related to Droplet snapshots"""

    def __init__(self, render):
        self.render = render
        self.region = Region(self.render)

    def __unique__(self, name):
        entries = self.list()
        if len(set(i.name for i in entries)) != len(entries):
            return False
        return True

    @debug
    def list(self):
        """List snapshots"""
        return self.render('images', '/images', params={
            'filter': 'my_images'
        })

    def show(self, name):
        """Show details for a single snapshot"""
        id = self.id_from_name(name)
        return self.render('image', '/images/%s' % id)

    @debug
    def transfer(self, name, region):
        id = self.id_from_name(name)
        region_id = self.region.id_from_name(region)

        try:
            return self.render('event_id', '/images/%s/transfer' % id, params={
                'region_id': region_id
            })
        except ClientException as e:
            raise ImageException(str(e))

    @debug
    def id_from_name(self, name):
        """Translate snapshot name into ID"""
        if not self.__unique__(name):
            raise SnapshotException("More than one snapshot matches %s" % name)
        res = next((
            r.id for r in self.list() if r.name.lower() == name.lower()),
            None)
        if res:
            return res
        raise SnapshotException('No snapshot called %s' % name)

    @debug
    def destroy(self, name):
        """Destroy snapshot"""
        try:
            id = self.id_from_name(name)
            return self.render('status', '/images/%s/destroy' % id)
        except ClientException as e:
            raise SnapshotException(str(e))
