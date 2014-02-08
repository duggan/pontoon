# -*- coding: utf-8 -*-

from . import debug
from .exceptions import ClientException
from .droplet import Droplet
from .event import Event
from .image import Image
from .region import Region
from .size import Size
from .snapshot import Snapshot
from .sshkey import SSHKey
from .mocking import _respond


API_HOST = 'api.digitalocean.com'
API_PORT = 80


class Struct:
    """
    A generic object for encapsulating response data.

    Accepts keyword arguments, translates them into attributes on the object.
    """
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Pontoon:
    """A user-created :class:`Pontoon <Pontoon>` object.

    Central interface to various pontoon objects.

    :param client_id: Digital Ocean API Client ID.
    :param api_key: Digital Ocean API key.
    :param host: HTTP URL for Digital Ocean API.
    :param port: Port to access host on.
    :param secure: Access API over HTTPS.
    :param mock: Use mocked request interface.

    Usage::

        >>> from pontoon import Pontoon
        >>> p = Pontoon('my_client_id', 'my_api_key')
        >>> p.droplet.list()
        [<pontoon.pontoon.Struct instance at 0x106ecf950>]
    """
    def __init__(self, client_id, api_key,
                 host=API_HOST, port=API_PORT, secure=True, mock=False):

        self.__mock = mock
        self.__client_id = client_id
        self.__api_key = api_key
        self.__port = port
        self.__host = host
        self.__secure = secure

        self.droplet = Droplet(self.render)
        self.event = Event(self.render)
        self.image = Image(self.render)
        self.region = Region(self.render)
        self.size = Size(self.render)
        self.snapshot = Snapshot(self.render)
        self.sshkey = SSHKey(self.render)

    @debug
    def render(self, key, path, method='GET', params={}):
        """
        Translates dictionary responses into
        :class:`Struct <Struct>` objects.

        :param key: top level key expected in a valid response.
        :param path: path fragment for API resource.
        :param method: HTTP verb for request.
        :param params: Parameters for request.
        """
        if self.__mock:
            self.request = _respond

        resp = self.request(path, method=method, params=params)

        if not resp:
            raise ClientException("Problem with request: "
                                  "%s, %s" % (path, params))
        content = resp.get(key, None)
        if type(content).__name__ == 'list':
            return [Struct(**r) for r in content]
        elif type(content).__name__ == 'dict':
            return Struct(**content)
        elif type(content).__name__ in ['str', 'int', 'unicode']:
            return content
        raise ClientException("Malformed response: %s" % content)

    @debug
    def request(self, path, method='GET', params={}):
        """Prepare and proxy to requests module."""
        import requests

        if method not in ['GET', 'POST']:
            raise ClientException("%s method not supported" % method)
        headers = {
            'User-Agent': 'pontoon/client'
        }

        params['client_id'] = self.__client_id
        params['api_key'] = self.__api_key

        url = self.get_url(path)

        if method == 'POST':
            headers['Content-Type'] = "application/json"
            response = requests.post(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            if response.json():
                json = response.json()
                error_msg = json.get('error_message', None)
                if error_msg:
                    raise ClientException(error_msg)
                return json
            raise ClientException('Empty json!')
        elif response.status_code == 401:
            raise ClientException('Access Denied')
        elif response.status_Code == 404:
            raise ClientException('Not Found')

        raise ClientException(('Status code: %d, full response: %s' %
                              (response.status_code, response.json())))

    def get_url(self, path):
        """Tranlsate path into a fully qualified URL."""
        port = "" if self.__port == 80 else ":%d" % self.__port
        protocol = "https://" if self.__secure else "http://"
        return "%s%s%s%s" % (protocol, self.__host, port, path)
