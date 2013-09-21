# -*- coding: utf-8 -*-

from . import configure, ui
from . import Pontoon


class Command:
    """
    Base class for CLI commands.

    Parses docstrings and initalizes client.
    """

    def __init__(self, doc, argv=None):
        from docopt import docopt

        configure.logger()
        conf = configure.combined()

        pontoon = Pontoon(conf['client_id'], conf['api_key'],
                          mock=configure.mock_mode)
        args = docopt(doc, argv=argv)

        self.pontoon = pontoon
        self.args = args

    def run(self, override=None):
        """Run the command specified by the docstring.

        :param override: Run a command other than the one specified.
        """

        if override is None:
            command = next(
                (k for k, v in self.args.items()
                    if k in dir(self) and v), None)
        else:
            command = override

        try:
            return getattr(self, command)()
        except (KeyboardInterrupt, EOFError):
            return 0
        except KeyError:
            ui.message("No command '%s'" % command)
        return 1
