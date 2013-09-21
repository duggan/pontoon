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

from pontoon import ui, configure
from pontoon import Command
from pontoon import SSHKeyException, ConfigureException


class SSHKeyCommand(Command):

    def list(self):
        keys = self.pontoon.sshkey.list()
        ui.message("Available SSH keys:")
        for s in keys:
            ui.message(" - %s" % s.name)
        return 0

    def add(self):
        ui.message("Creating %s using key at %s..." % (
            self.args['<name>'], self.args['<public-key-path>']))
        try:
            public_key = configure.read_key(self.args['<public-key-path>'])
        except ConfigureException as e:
            raise SSHKeyException(str(e))

        self.pontoon.sshkey.add(self.args['<name>'], public_key)

    def show(self):
        try:
            result = self.pontoon.sshkey.show(self.args['<name>'])
            ui.message(result.ssh_pub_key)
            return 0
        except SSHKeyException:
            ui.message("No such key '%s'" % self.args['<name>'])
            return 1

    def replace(self):
        ui.message("Replacing contents of %s using key at %s..." % (
            self.args['<name>'], self.args['<public-key-path>']))
        public_key = configure.read_key(self.args['<public-key-path>'])
        self.pontoon.sshkey.replace(self.args['<name>'], public_key)

    def destroy(self):
        ui.message("Destroying %s..." % self.args['<name>'])
        self.pontoon.sshkey.destroy(self.args['<name>'])


if __name__ == '__main__':

    try:
        cmd = SSHKeyCommand(str(__doc__))
        exit(cmd.run())
    except SSHKeyException as e:
        ui.message(str(e))
        exit(1)

    exit(0)
