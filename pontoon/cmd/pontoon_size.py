#!/usr/bin/env python

"""Usage: pontoon size list

Options:
    -h --help       Show this page.
"""

from docopt import docopt
from ..lib import Manager, Size
from .. import configure, ui
from ..command import Command
from .. import MOCK


class SizeCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def list(self):
        available = self.manager.get_all_sizes()
        ui.message("Available sizes:")
        for s in available:
            ui.message(" - %s" % s.slug)
        return 0


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__))

        exit(SizeCommand(config, args).run())

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
