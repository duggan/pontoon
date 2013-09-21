# -*- coding: utf-8 -*-


class PontoonException(Exception):
    """An ambiguous error occurred while handling the command"""


class ClientException(PontoonException):
    """An error occurred during the API request"""


class APIException(PontoonException):
    """An error occurred while processing the API request"""


class SnapshotException(PontoonException):
    """An error occurred while processing the snapshot"""


class DropletException(PontoonException):
    """An error occurred managing the Droplet"""


class ConfigureException(PontoonException):
    """An error occurred while processing the configuration file"""


class SSHKeyException(PontoonException):
    """An error occurred processing the SSH key command"""


class ImageException(PontoonException):
    """An error occurred processing the image commnad"""


class RegionException(PontoonException):
    """An error occurred processing the region command"""


class SizeException(PontoonException):
    """An error occurred processing the size command"""


class EventException(PontoonException):
    """An error occurred processing the event"""
