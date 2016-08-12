# -*- coding: utf-8 -*-

from . import ui


class Command:
    """
    Base class for CLI commands.

    Parses docstrings and initalizes client.
    """

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
            method = getattr(self, command)
        except KeyError:
            ui.message("No command '%s'" % command)
            return 1
        try:
            return method()
        except (KeyboardInterrupt, EOFError):
            return 0
        return 1
