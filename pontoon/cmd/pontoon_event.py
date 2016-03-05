#!/usr/bin/env python

"""Usage: pontoon event show <id>

Options:
    -h --help       Show this page.
"""

from docopt import docopt
from ..lib import Manager
from .. import ui, configure
from ..command import Command
from .. import MOCK


class EventCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def show(self):
        action = self.manager.get_action(self.args['<id>'])
        details = ui.format_event(action)

        ui.message("Event %s" % self.args['<id>'])
        for k, v in details.items():
            ui.message("   %s: %s" % (k, v))
        return 0


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__))

        exit(EventCommand(config, args).run())

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
