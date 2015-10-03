#!/usr/bin/env python

"""Pontoon. A Python CLI for Digital Ocean.

Usage:
    pontoon <command> [<args>...]
    [--version]
    [--help]

The top level pontoon commands are:
    configure   Interactive configuration for pontoon
    droplet     Interact with Droplets
    event       Events on or around Droplets
    image       Public machine images available for Droplets
    region      Regions for Droplets
    size        Droplet sizes
    snapshot    Private snapshots created
    sshkey      SSH key management

See 'pontoon help <command>' for more information on a specific command.

"""

from subprocess import call
from docopt import docopt
from ..meta import __version__
from .. import ui


def main():
    args = docopt(__doc__,
                  version=__version__,
                  options_first=True)

    argv = [args['<command>']] + args['<args>']
    try:
        if args['<command>'] in ['help', None]:
            if not args['<args>']:
                return call(['pontoon', '--help'])
            return call(['pontoon-%s' % args['<args>'][0], '--help'])
        else:
            return call(['pontoon-%s' % args['<command>']] + argv)
    except (KeyboardInterrupt, EOFError):
        return 0
    except OSError:
        ui.message("No command '%s'" % args['<command>'])
    return 1


if __name__ == '__main__':
    exit(main())
