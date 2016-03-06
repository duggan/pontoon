#!/usr/bin/env python

"""Usage: pontoon region list

Options:
    -h --help       Show this page.
"""

from docopt import docopt
from ..lib import Manager, Region
from .. import configure, ui
from ..command import Command
from .. import MOCK


class RegionCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def list(self):
        available = self.manager.get_all_regions()
        ui.message("Available regions:")
        ui.message("   %-20s %s" % ("name", "slug"))
        ui.line(length=30)

        for s in available:
            ui.message(" - %-20s (%s)" % (s.name, s.slug))
        return 0


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__))

        exit(RegionCommand(config, args).run())

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
