# -*- coding: utf-8 -*-


class PontoonException(Exception):
    """An ambiguous error occurred while handling the command"""


class ConfigureException(PontoonException):
    """An error occurred while processing the configuration file"""
