.. _api:

Developer Interface
===================

.. module:: pontoon

This part of the documentation covers all the interfaces of Pontoon.


Pontoon Class
-------------

The Pontoon interface is the main entry point for using the library
as a developer.

.. autoclass:: pontoon.pontoon.Pontoon
   :members:
   :private-members:
   :undoc-members:

Droplet Class
-------------

.. autoclass:: pontoon.droplet.Droplet
   :members:
   :private-members:
   :undoc-members:

Event Class
-----------

.. autoclass:: pontoon.event.Event
   :members:
   :private-members:
   :undoc-members:

Image Class
-----------

.. autoclass:: pontoon.image.Image
   :members:
   :private-members:
   :undoc-members:

Region Class
------------

.. autoclass:: pontoon.region.Region
   :members:
   :private-members:
   :undoc-members:

Size Class
----------

.. autoclass:: pontoon.size.Size
   :members:
   :private-members:
   :undoc-members:

Snapshot Class
--------------

.. autoclass:: pontoon.snapshot.Snapshot
   :members:
   :private-members:
   :undoc-members:

SSH Key Class
-------------

.. autoclass:: pontoon.sshkey.SSHKey
   :members:
   :private-members:
   :undoc-members:

UI module
---------

This module handles all output for the CLI, as well as some
filesystem interactions. This is the only location outside of tests
where the print statement is invoked directly.

.. automodule:: pontoon.ui
   :members:
   :private-members:
   :undoc-members:

Mocking Module
--------------

.. automodule:: pontoon.mocking
   :members:
   :private-members:
   :undoc-members:

Log Module
----------

.. automodule:: pontoon.log
   :members:
   :private-members:
   :undoc-members:

Exceptions
----------

.. automodule:: pontoon.exceptions
   :members:
   :private-members:
   :undoc-members:

Configure Module
----------------

The configure module is a collection of methods for handling interaction
with some external tools, config files, and for interactive configuration.

.. automodule:: pontoon.configure
    :members:
    :private-members:
    :undoc-members:

Command Class
-------------

The Command class encapsulates plumbing common to all CLI commands.

.. autoclass:: pontoon.command.Command
    :members:
    :private-members:
    :undoc-members:
