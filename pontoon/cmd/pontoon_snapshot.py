#!/usr/bin/env python

"""Usage:
          pontoon snapshot list [--with-ids]
          pontoon snapshot show <name>
          pontoon snapshot destroy <name>
          pontoon snapshot transfer <name> <region>

Options:
    --with-ids      Include ids in output. Useful for other software that uses
                    Digital Ocean ids for input (like Packer).
    -h --help       Show this page.
"""

from .. import ui
from .. import Command
from .. import SnapshotException


class SnapshotCommand(Command):

    def list(self):
        available = self.pontoon.snapshot.list()
        ui.message("Available snapshots:")
        if len(set(s.name for s in available)) != len(available):
            ui.warning("Warning: multiple snapshots have the same name! "
                       "Actions on these snapshots will fail until this is "
                       "resolved in the web UI.")

        for s in available:
            if self.args['--with-ids']:
                ui.message(" - %-10s %s" % (str(s.id) + ':', s.name))
            else:
                ui.message(" - %s" % s.name)
        return 0

    def show(self):
        img = self.pontoon.snapshot.show(self.args['<name>'])
        for k, v in img.__dict__.items():
            ui.message("   %s: %s" % (k, v))

    def destroy(self):
        ui.message("Destroying %s..." % self.args['<name>'])
        self.pontoon.snapshot.destroy(self.args['<name>'])

    def transfer(self):
        ui.message("Transferring %s to %s..." % (
            self.args['<name>'],
            self.args['<region>']
        ))
        self.pontoon.snapshot.transfer(self.args['<name>'],
                                       self.args['<region>'])
        return 0


def main():
    try:
        cmd = SnapshotCommand(str(__doc__))
        exit(cmd.run())
    except SnapshotException as e:
        ui.message(str(e))
        exit(1)

    exit(0)

if __name__ == '__main__':
    main()
