#!/usr/bin/env python

"""Usage: pontoon size list [--with-ids]

Options:
    --with-ids      Include ids in output. Useful for other software that uses
                    Digital Ocean ids for input (like Packer).
    -h --help       Show this page.
"""

from .. import ui
from .. import Command
from .. import SizeException


class SizeCommand(Command):

    def list(self):
        available = self.pontoon.size.list()
        ui.message("Available sizes:")
        for s in available:
            if self.args['--with-ids']:
                ui.message(" - %-10s %s" % (str(s.id) + ':', s.name))
            else:
                ui.message(" - %s" % s.name)
        return 0


def main():
    try:
        cmd = SizeCommand(str(__doc__))
        exit(cmd.run())
    except SizeException as e:
        ui.message(str(e))
        exit(1)

    exit(0)

if __name__ == '__main__':
    main()
