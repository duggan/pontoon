# -*- coding: utf-8 -*-

from .exceptions import ClientException, SSHKeyException
from . import debug, cache


class SSHKey:
    """Manage operations related to SSH keys"""

    def __init__(self, render):
        self.render = render

    @cache
    def list(self):
        """List registered SSH keys"""
        try:
            return [s for s in self.render('ssh_keys', '/ssh_keys')]
        except ClientException as e:
            raise SSHKeyException(str(e))

    @debug
    def show(self, name):
        """Retrieve SSH key details (including public portion of key)"""
        id = self.id_from_name(name)
        try:
            return self.render('ssh_key', '/ssh_keys/%s' % id)
        except ClientException as e:
            raise SSHKeyException(str(e))

    @debug
    def add(self, name, public_key):
        """Register a public key with your Digital Ocean account"""
        if name not in [s.name for s in self.list()]:
            try:
                return self.render('ssh_key', '/ssh_keys/new', params={
                    'name': name,
                    'ssh_pub_key': public_key
                })
            except ClientException as e:
                raise SSHKeyException(str(e))
        raise SSHKeyException("Aborted: this would create two "
                              "keys with the same name.")

    @debug
    def replace(self, name, public_key):
        """Replace a registered SSH key"""
        id = self.id_from_name(name)
        params = {
            'ssh_pub_key': public_key
        }
        try:
            return self.render('ssh_key', '/ssh_keys/%s/edit' % id,
                               params=params)
        except ClientException as e:
            raise SSHKeyException(str(e))

    @debug
    def destroy(self, name):
        """Deresgister an SSH key"""
        id = self.id_from_name(name)
        try:
            return self.render('status', '/ssh_keys/%s/destroy' % id)
        except ClientException as e:
            raise SSHKeyException(str(e))

    @cache
    @debug
    def id_from_name(self, name):
        """Tranlsate an SSH key name into its ID"""
        ret = next((r.id for r in self.list() if r.name == name), None)
        if ret:
            return ret
        raise SSHKeyException("No key found called %s" % name)

    @cache
    @debug
    def name_from_id(self, id):
        """Translate an SSH key id into its name"""
        ret = next((r.name for r in self.list() if r.id == id), None)
        if ret:
            return ret
        raise SSHKeyException("No key found for id %s" % id)
