#!/usr/bin/env python

"""Usage: pontoon region list [--with-ids]

Options:
    --with-ids      Include ids in output. Useful for other software that uses
                    Digital Ocean ids for input (like Packer).
    -h --help       Show this page.
"""

from pontoon import ui
from pontoon import Command
from pontoon import RegionException


class RegionCommand(Command):

    def list(self):
        available = self.pontoon.region.list()
        ui.message("Available regions:")
        for r in available:
            if self.args['--with-ids']:
                ui.message(" - %-10s %s" % (str(r.id) + ':', r.name))
            else:
                ui.message(" - %s" % r.name)
        return 0


if __name__ == '__main__':

    try:
        cmd = RegionCommand(str(__doc__))
        exit(cmd.run())
    except RegionException as e:
        ui.message(str(e))
        exit(1)

    exit(0)
