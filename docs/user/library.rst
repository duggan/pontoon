Library Usage
=============

To use pontoon as a library, install from pip, and use like so:

::

    >>> from pontoon import Pontoon
    >>> pontoon = Pontoon('my-client-id', 'my-api-key')
    >>> pontoon.droplet.list()
    [<pontoon.pontoon.Struct instance at 0x106ecf950>]

The library component owes its genesis to
`DOP <https://github.com/ahmontero/dop>`__, by Antonio Hinojo.

