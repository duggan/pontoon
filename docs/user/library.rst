Library Usage
=============

To use pontoon's bundled library, install from pip, and use like so:

::

    >>> import pontoon.lib
    >>> manager = pontoon.lib.Manager(token="secretspecialuniquesnowflake")
    >>> droplets = manager.get_all_droplets()
    >>> for droplet in my_droplets:
    >>>    droplet.shutdown()

The library is a fork of `python-digitalocean <https://github.com/koalalorenzo/python-digitalocean>`__, by Lorenzo Setale.

Further documentation for the library can be found there!
