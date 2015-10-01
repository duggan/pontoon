# -*- coding: utf-8 -*-

from .exceptions import ClientException, DropletException
from . import debug, cache
from .snapshot import Snapshot
from .size import Size
from .region import Region
from .image import Image
from .sshkey import SSHKey


class Droplet:

    """Manage operations related to Droplets."""

    def __init__(self, render):
        self.render = render
        self.snap = Snapshot(self.render)
        self.size = Size(self.render)
        self.region = Region(self.render)
        self.image = Image(self.render)
        self.sshkey = SSHKey(self.render)

    def __unique__(self, name):
        entries = self.list()
        if len(set(i.name for i in entries)) != len(entries):
            return False
        return True

    @debug
    def list(self):
        """Return a list of Droplets."""
        try:
            return self.render('droplets', '/droplets')
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def id_from_name(self, name):
        """Tranlate a hostname into its Droplet ID."""
        if not self.__unique__(name):
            raise DropletException("More than one Droplet matches %s" % name)
        res = next((
            r.id for r in self.list() if r.name.lower() == name.lower()),
            None)
        if res:
            return res
        raise DropletException('No Droplet found')

    @debug
    def name_from_id(self, id):
        """Translate a Droplet ID into its hostname."""
        try:
            return self.render('droplet', '/droplets/%s' % id).name
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def show(self, name):
        """Retrieve information about a single Droplet."""
        id = next((d.id for d in self.list() if d.name == name), None)

        try:
            return self.render('droplet', '/droplets/%s' % id)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def create(self, name=None, size=None, image=None,
               region=None, keys=None, disable_virtio=False,
               private_networking=False):
        """
        Create a Droplet. Returns a :class:`Struct <Struct>` object.

        :param name: Hostname for Droplet.
        :param size: Size of Droplet (512MB, 1GB...)
        :param image: Image to use for Droplet.
        :param region: Region to boot Droplet in.
        :param keys: List of registered SSH keys to associate with Droplet.
        :param disable_virtio: Disable VirtIO for Droplet (not recommended).
        :param private_networking: Add a private IP (if available).
        """

        if (name and size and image and region) is None:
            raise DropletException("Name, size, image and region "
                                   "are all required.")

        virtio = False if disable_virtio else True

        if name in [d.name for d in self.list()]:
            raise DropletException(
                'This would create two droplets with the same hostname.')

        # keys should be a empty list, instead of None if nothing is passed
        # as later it is iterated upon, without this error is raised.
        if keys is None:
            keys = []

        size_id = self.size.id_from_name(size)
        image_id = self.image.id_from_name(image)
        region_id = self.region.id_from_name(region)
        ssh_key_ids = [
            k.id for k in self.sshkey.list() if k.name.lower() in [
                n for n in keys]]

        params = {
            'name': name,
            'size_id': size_id,
            'image_id': image_id,
            'region_id': region_id,
        }

        if ssh_key_ids:
            params['ssh_key_ids'] = ','.join([str(k) for k in ssh_key_ids])
        if virtio:
            params['virtio'] = 1
        if private_networking:
            params['private_networking'] = 1

        try:
            return self.render('droplet', '/droplets/new', params=params)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def start(self, name):
        """Boot Droplet"""
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/power_on' % id)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def shutdown(self, name):
        """Send ACPI shutdown signal to Droplet"""
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/shutdown' % id,
                               method='POST')
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def snapshot(self, name, snapshot_name):
        """Create a snapshot of the Droplet (must be shut down first)"""
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/snapshot' % id,
                               params={'name': snapshot_name})
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def restore(self, droplet_name, snapshot_name):
        """Restore Droplet from a snapshot (must be shut down first)"""

        droplet_id = self.id_from_name(droplet_name)
        snapshot_id = self.snap.id_from_name(snapshot_name)

        try:
            return self.render('event_id', '/droplets/%s/restore' % (
                droplet_id), params={'image_id': snapshot_id})
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def rebuild(self, droplet_name, image_name):
        """Rebuild Droplet from a stock image (must be shut down first)"""
        droplet_id = self.id_from_name(droplet_name)
        image_id = self.image.id_from_name(image_name)

        return self.render('event_id', '/droplets/%s/rebuild' % (droplet_id),
                           params={'image_id': image_id})

    @debug
    def rename(self, frm, to):
        """Rename Droplet (must be shut down first)"""
        from_id = self.id_from_name(frm)
        if to not in [d.name for d in self.list()]:
            try:
                return self.render('event_id', '/droplets/%s/rename' % from_id,
                                   params={'name': to})
            except ClientException as e:
                raise DropletException(str(e))
        raise DropletException("There is already a Droplet named '%s'" % to)

    @debug
    def resize(self, name, size):
        """Resize Droplet (must be shut down first)"""
        id = self.id_from_name(name)
        size_id = self.size.id_from_name(size)
        try:
            return self.render('event_id', '/droplets/%s/resize' % id,
                               params={'size_id': size_id})
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def destroy(self, name, no_scrub=False):
        """Destroy Droplet"""
        id = self.id_from_name(name)
        scrub_data = False if no_scrub else True
        try:
            return self.render('event_id', '/droplets/%s/destroy' % id,
                               params={'scrub_data': 1 if scrub_data else 0})
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def status(self, name):
        """Retrive Droplet status"""
        id = self.id_from_name(name)
        try:
            return self.render('droplet', '/droplets/%s' % id).status
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def reboot(self, name):
        """Reboot Droplet"""
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/reboot' % id)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def powercycle(self, name):
        """Power cycle Droplet"""
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/power_cycle' % id)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def poweroff(self, name):
        """Power down Droplet"""
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/power_off' % id)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def backups(self, action, name):
        """
        Enable or disable backups for Droplet

        :param action: either 'enable' or 'disable'
        :param name: Name of Droplet
        """
        id = self.id_from_name(name)
        try:
            if action == 'enable':
                return self.render('event_id',
                                   '/droplets/%s/enable_backups' % id)
            elif action == 'disable':
                return self.render('event_id',
                                   '/droplets/%s/disable_backups' % id)
        except ClientException as e:
            raise DropletException(str(e))

    @debug
    def passwordreset(self, name):
        """
        Reset root password for Droplet
        (results in email to registered Digital Ocean account)
        """
        id = self.id_from_name(name)
        try:
            return self.render('event_id', '/droplets/%s/password_reset' % id)
        except ClientException as e:
            raise DropletException(str(e))
