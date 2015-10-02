#!/usr/bin/env python

"""Usage: pontoon event show <id>

Options:
    -h --help       Show this page.
"""

from pontoon import ui
from pontoon import Command
from pontoon import EventException


class EventCommand(Command):

    def show(self):
        ev = self.pontoon.event.show(self.args['<id>'])
        ev = ui.format_event(
            ev,
            type=self.pontoon.event.type_from_id(ev.event_type_id),
            droplet=self.pontoon.droplet.name_from_id(ev.droplet_id))

        ui.message("Event %s" % self.args['<id>'])
        for k, v in ev.items():
            ui.message("   %s: %s" % (k, v))
        return 0


if __name__ == '__main__':

    try:
        cmd = EventCommand(str(__doc__))
        exit(cmd.run())
    except EventException as e:
        ui.message(str(e))
        exit(1)

    exit(0)
