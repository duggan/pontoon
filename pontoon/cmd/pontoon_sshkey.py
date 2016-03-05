#!/usr/bin/env python

"""Usage:
          pontoon sshkey list
          pontoon sshkey add <name> <public-key-path>
          pontoon sshkey show <name>
          pontoon sshkey replace <name> <public-key-path>
          pontoon sshkey destroy <name>

Options:
    -h --help       Show this page.
"""

from docopt import docopt
from ..lib import Manager, SSHKey
from .. import configure, ui
from ..command import Command
from .. import MOCK


class SSHKeyCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def _get_sshkey(self, name):
        resources = self.manager.get_all_sshkeys()
        resource = [res for res in resources if res.name == name]

        if len(resource) > 1:
            ui.warning("Warning: multiple SSH keys with identical "
                       "names found. Actions on those keys "
                       "will fail until this is resolved in the web UI.")
            raise Exception("Multiple SSH keys named '%s'" % name)

        if len(resource) == 0:
            raise Exception("No SSH key named '%s'" % name)

        return resource[0]

    def list(self):
        keys = self.manager.get_all_sshkeys()
        ui.message("Available SSH keys:")
        for s in keys:
            ui.message(" - %s" % s.name)
        return 0

    def add(self):
        ui.message("Creating %s using key at %s..." % (
            self.args['<name>'], self.args['<public-key-path>']))

        public_key = configure.read_key(self.args['<public-key-path>'])
        sshkey = SSHKey(token=self.config['api_token'], mocked=MOCK)
        if not sshkey.load_by_pub_key(public_key):
            sshkey.name = self.args['<name>']
            sshkey.public_key = public_key
            sshkey.create()

    def show(self):
        key = self._get_sshkey(self.args['<name>'])
        ui.message(key.public_key)

    def replace(self):
        ui.message("Replacing contents of %s using key at %s..." % (
            self.args['<name>'], self.args['<public-key-path>']))
        public_key = configure.read_key(self.args['<public-key-path>'])

        sshkey = self._get_sshkey(self.args['<name>'])
        sshkey.public_key = public_key
        sshkey.edit()

    def destroy(self):
        ui.message("Destroying %s..." % self.args['<name>'])
        sshkey = self._get_sshkey(self.args['<name>'])
        sshkey.destroy()


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__))

        exit(SSHKeyCommand(config, args).run())

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
