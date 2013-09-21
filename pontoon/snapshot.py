# -*- coding: utf-8 -*-

from .exceptions import ClientException, SnapshotException
from . import debug, cache
from .region import Region


class Snapshot:
    """Manage operations related to Droplet snapshots"""

    def __init__(self, render):
        self.render = render
        self.region = Region(self.render)

    @cache
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
        matches = [s.id for s in self.list() if s.name.lower() == name.lower()]
        if len(matches) == 0:
            raise SnapshotException('No snapshot named "%s" found' % name)
        elif len(matches) == 1:
            return matches[0]
        else:
            raise SnapshotException('More than one match for "%s"' % name)

    @debug
    def destroy(self, name):
        """Destroy snapshot"""
        id = self.id_from_name(name)
        return self.render('event', '/images/%s/destroy' % id)
