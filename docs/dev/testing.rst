Contributing
------------

Pull requests for bugs are always welcome! New functionality should
generally be preceded by a discussion, though if you've written
something that you needed and want to contribute back, a pull request is
a fine way to start that discussion :)

All of the code in pontoon is
`PEP-8 <http://www.python.org/dev/peps/pep-0008/>`__ audited (using
`pytest-pep8 <https://pypi.python.org/pypi/pytest-pep8>`__), and there's
a full suite of tests written for `py.test <http://pytest.org/>`__
(library code) and `Bats <https://github.com/sstephenson/bats>`__
(interface). Contributions should, therefore, include tests and pass a
PEP-8 audit.

Running the tests
~~~~~~~~~~~~~~~~~

Running the tests locally requires the contents of ``requirements.txt``
as well as bats.

::

    $ pip install -r requirements.txt

On OSX, bats can be installed with homebrew:

::

    $ brew install bats

On Debian/Ubuntu, I've set up a PPA for easy installation of bats:

::

    $ add-apt-repository ppa:duggan/bats
    $ apt-get update
    $ apt-get install bats

Tests can then be run from the root directory:

::

    $ py.test --pep8 --cov pontoon
    $ bats test/bats

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

This is implemented soley for end-to-end testing of the CLI, but you may
find it useful in some other scenarios.

Addendum
--------

Windows support
~~~~~~~~~~~~~~~

Pontoon's lack of Windows support is a bug, not a feature. If you need
pontoon on Windows, the best way to help get it there is with a pull
request.
