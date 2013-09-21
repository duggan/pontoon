# -*- coding: utf-8 -*-

from .exceptions import ClientException, EventException
from . import debug, cache


class Event:
    """Manage operations related to events"""

    def __init__(self, render):
        self.render = render

    @debug
    def show(self, id):
        """Show details for a single event"""
        try:
            return self.render('event', '/events/%s' % id)
        except ClientException as e:
            raise EventException(str(e))

    @debug
    def type_from_id(self, id):
        """Tranlate event type IDs into something human readable."""
        # There should be an API endpoint for this
        # but let's pretend there is until there is.
        types = {
            8: 'snapshot',
        }
        if id in types:
            return types[id]
        return "unknown (%s)" % id
