#!/usr/bin/env python

"""Usage:
          pontoon image list [--with-ids]
          pontoon image oses
          pontoon image show <name>

Options:
    --with-ids      Include ids in output. Useful for other software that uses
                    Digital Ocean ids for input (like Packer).
    -h --help       Show this page.
"""

from .. import ui
from .. import Command
from .. import ImageException


class ImageCommand(Command):

    def list(self):
        available = self.pontoon.image.list()
        ui.message("Available images:")
        for s in available:
            if self.args['--with-ids']:
                ui.message(" - %-10s %s" % (str(s.id) + ':', s.name))
            else:
                ui.message(" - %s" % s.name)
        return 0

    def show(self):
        img = self.pontoon.image.show(self.args['<name>'])
        for k, v in img.__dict__.items():
            ui.message("   %s: %s" % (k, v))

    def oses(self):
        available = self.pontoon.image.oses()
        ui.message("Available Operating Systems:")
        for o in available:
            ui.message(" - %s" % o)
        return 0


if __name__ == '__main__':

    try:
        cmd = ImageCommand(str(__doc__))
        exit(cmd.run())
    except ImageException as e:
        ui.message(str(e))
        exit(1)

    exit(0)
