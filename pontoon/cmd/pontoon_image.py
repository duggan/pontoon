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

from docopt import docopt
from ..lib import Manager, Image
from .. import configure, ui
from ..command import Command
from .. import MOCK


class ImageCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def _get_image(self, name):
        resources = self.manager.get_all_images()
        resource = [res for res in resources if res.name == name]

        if len(resource) > 1:
            ui.warning("Warning: multiple images with identical "
                       "names found. Actions on those images "
                       "will fail until this is resolved in the web UI.")
            raise Exception("Multiple images named '%s'" % name)

        if len(resource) == 0:
            raise Exception("No image named '%s'" % name)

        return resource[0]

    def list(self):
        available = self.manager.get_all_images()
        ui.message("Available images:")
        if self.args['--with-ids']:
            ui.message("   %-10s %-10s %-45s %s" % (
                       "id", "distro", "name", "slug"))
            ui.line(length=80)
        else:
            ui.message("   %-10s %-45s %s" % ("distro", "name", "slug"))
            ui.line(length=80)

        for s in available:
            if self.args['--with-ids']:
                name = s.name[:27] + "..." if len(s.name) > 30 else s.name
                ui.message(" - %-10s %-10s %-35s %s" % (
                           str(s.id) + ':', s.distribution, name,
                           s.slug or ''))
            else:
                name = s.name[:37] + "..." if len(s.name) > 40 else s.name
                ui.message(" - %-10s %-45s %s" % (
                           s.distribution, name, s.slug or ''))
        return 0

    def show(self):
        image = self._get_image(self.args['<name>'])
        details = ui.format_item(image)
        ui.yaml_message(details)

    def oses(self):
        available = self.manager.get_all_images()
        ui.message("Available Operating Systems:")
        oses = []
        for image in available:
            if image.distribution not in oses:
                oses.append(image.distribution)
        for os in oses:
            ui.message(" - %s" % os)
        return 0


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__))

        exit(ImageCommand(config, args).run())

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
