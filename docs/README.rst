pontoon
=======

A Python CLI (and library) for `Digital
Ocean <https://digitalocean.com>`__.

Introduction
------------

Pontoon makes interacting with Digital Ocean on the command line smooth
sailing.

It is designed for human consumption, and aims to have good defaults.

It also happens to be a library.

Caveats
-------

Pontoon has one rule it imposes on top of Digital Ocean:

***Names are unique.***

Unique names make for a much easier command line experience. For
Droplets, names are hostnames, and hostnames should be unique anyway;
it's just a good idea.

They don't have to be unique *forever* though; once a Droplet is
destroyed, it's fine to use the name again.

Anything "recommended" (like secure-erasing the drive on termination) is
optional, but enabled by default.

Installation
------------

Install via pip:

::

    $ pip install pontoon

To install the latest (development, unstable) release:

::

    $ pip install https://github.com/duggan/pontoon/archive/master.zip

If you'd like to package pontoon for your favourite OS, feel free to do
so (and please send a PR to this README!)

More options are on the way.

CLI Usage
---------

Configure
~~~~~~~~~

Set up your credentials and preferences:

::

    $ pontoon configure

You'll be prompted for your Digital Ocean API credentials (`available
here <https://cloud.digitalocean.com/api_access>`__), and whether you
want to use existing SSH credentials or for them to be generated (using
OpenSSH).

The rest are preferences, and can be set at any time by running
configure again, editing the ``~/.pontoon`` config file (YAML format),
or by specifying them with options on the command line.

Create your first Droplet!
~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can create your first droplet:

::

    $ pontoon droplet create foobar
    Creating Droplet foobar (512MB using Ubuntu 12.04 x64 in Amsterdam 1)...
    .......active

SSH into your Droplet
~~~~~~~~~~~~~~~~~~~~~

If everything's configured correctly, you should be able to SSH into
your Droplet like so:

::

    $ pontoon droplet ssh foobar
    Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-virtual x86_64)

     * Documentation:  https://help.ubuntu.com/
    Last login: Fri May  3 18:23:56 2013
    root@foobar:~#

List your Droplets
~~~~~~~~~~~~~~~~~~

::

    $ pontoon droplet list
    foobar:         (512MB, Ubuntu 12.04 x64, Amsterdam 1, 192.0.2.128, active)

or for more detail:

::

    $ pontoon droplet list --detail
    foobar
       id:                  998
       name:                foobar
       size:                512MB
       image:               Ubuntu 12.04 x64
       region:              Amsterdam 1
       status:              active
       locked:              False
       private_ip_address:  None
       created_at:          2013-11-09T13:22:40Z
       backups_active:      False
       ip_address:          192.0.2.128

Contributing
------------

Pull requests for bugs are always welcome! New functionality should
generally be preceded by a discussion, though if you've written
something that you needed and want to contribute back, a pull request is
a fine way to start that discussion :tada:

All of the code in pontoon is
`PEP-8 <http://www.python.org/dev/peps/pep-0008/>`__ audited (using
`pytest-pep8 <https://pypi.python.org/pypi/pytest-pep8>`__), and there's
a full suite of tests written for `py.test <http://pytest.org/>`__
(library code) and `Bats <https://github.com/sstephenson/bats>`__
(interface). Contributions should, therefore, include tests and pass a
PEP-8 audit.

Running the tests
~~~~~~~~~~~~~~~~~

Tests are run via `Tox <https://tox.readthedocs.org>`__.

For example, to test the library, CLI and coverage for Python 2.7, run:

::

    $ pip install tox
    $ tox -e py27,lib,cli,coverage

The ``.travis.yml`` file in this repository enumerates all the tests
that are performed.

The CLI tests require `BATS <https://github.com/sstephenson/bats>`__,
and PEP8 checks are performed in both the ``lib`` tests and ``cli``
tests.

On OSX, bats can be installed with homebrew:

::

    $ brew install bats

On Debian/Ubuntu, I've set up a PPA for easy installation of bats:

::

    $ add-apt-repository ppa:duggan/bats
    $ apt-get update
    $ apt-get install bats

Debugging
~~~~~~~~~

Set the ``DEBUG`` environment variable (to anything) to enable debug
output for pontoon.

This will give a step through of most methods being executed during a
command, like so:

::

    $ DEBUG=1 pontoon droplet destroy foobar
    2013-11-09 18:37:06,187 [pontoon.configure:DEBUG] combined: (){}
    2013-11-09 18:37:06,187 [pontoon.configure:DEBUG] read_config: (){}
    Destroying foobar and scrubbing data...
    2013-11-09 18:37:06,204 [pontoon.droplet:DEBUG] destroy: (<pontoon.droplet.Droplet instance at 0x10ce1fd40>, 'foobar', False){}
    2013-11-09 18:37:06,204 [pontoon.droplet:DEBUG] id_from_name: (<pontoon.droplet.Droplet instance at 0x10ce1fd40>, 'foobar'){}
    2013-11-09 18:37:06,204 [pontoon.droplet:DEBUG] list: (<pontoon.droplet.Droplet instance at 0x10ce1fd40>,){}
    2013-11-09 18:37:06,205 [pontoon.pontoon:DEBUG] render: (<pontoon.pontoon.Pontoon instance at 0x10ce1fcf8>, 'droplets', '/droplets'){}
    2013-11-09 18:37:06,205 [pontoon.pontoon:DEBUG] request: (<pontoon.pontoon.Pontoon instance at 0x10ce1fcf8>, '/droplets'){'params': {}, 'method': 'GET'}
    2013-11-09 18:37:07,498 [pontoon.pontoon:DEBUG] render: (<pontoon.pontoon.Pontoon instance at 0x10ce1fcf8>, 'event_id', '/droplets/998/destroy'){'params': {'scrub_data': 1}}
    2013-11-09 18:37:07,498 [pontoon.pontoon:DEBUG] request: (<pontoon.pontoon.Pontoon instance at 0x10ce1fcf8>, '/droplets/998/destroy'){'params': {'scrub_data': 1}, 'method': 'GET'}

A timestamp, followed by the module, debug level, the method called and
the arguments to that method (positional as brackets, keywords as
curlies).

This functionality is implemented by the ``@debug`` decorator, the code
for which can be seen at ``pontoon/log.py``.

Mocking
~~~~~~~

Set the ``MOCK`` environment variable (to anything) to return mock
request data instead of querying Digital Ocean.

This is implemented solely for end-to-end testing of the CLI, but you may
find it useful in some other scenarios.

.. |Build Status on Linux| image:: https://travis-ci.org/duggan/pontoon.png?branch=master
   :target: https://travis-ci.org/duggan/pontoon
.. |Build status on Windows| image:: https://ci.appveyor.com/api/projects/status/rljdp3isvaj2pl3q?svg=true
   :target: https://ci.appveyor.com/project/duggan/pontoon
.. |Coverage Status| image:: https://coveralls.io/repos/duggan/pontoon/badge.png?branch=master
   :target: https://coveralls.io/r/duggan/pontoon?branch=master
.. |Doc Status| image:: https://readthedocs.org/projects/pontoon/badge/?version=latest
   :target: http://pontoon.readthedocs.org/en/latest/?badge=latest

