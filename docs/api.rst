.. _api:

Developer Interface
===================

.. module:: pontoon

This part of the documentation covers all the interfaces of Pontoon.


Library Module
-------------

pontoon.lib is the main entry point for using the library
as a developer.

.. automodule:: pontoon.lib
   :members:

Manager Class
-------------

.. autoclass:: pontoon.lib.Manager
   :members:
   :private-members:

Droplet Class
-------------

.. autoclass:: pontoon.lib.Droplet
   :members:
   :private-members:

Account Class
-------------

.. autoclass:: pontoon.lib.Account
   :members:
   :private-members:

Action Class
------------

.. autoclass:: pontoon.lib.Action
   :members:
   :private-members:

Domain Class
------------

.. autoclass:: pontoon.lib.Domain
   :members:
   :private-members:
   :undoc-members:

FloatingIP Class
----------------

.. autoclass:: pontoon.lib.FloatingIP
   :members:
   :private-members:
   :undoc-members:

Image Class
-----------

.. autoclass:: pontoon.lib.Image
   :members:
   :private-members:

Kernel Class
------------

.. autoclass:: pontoon.lib.Kernel
   :members:
   :private-members:

Record Class
------------

.. autoclass:: pontoon.lib.Record
   :members:
   :private-members:

Region Class
------------

.. autoclass:: pontoon.lib.Region
   :members:
   :private-members:

SSHKey Class
------------

.. autoclass:: pontoon.lib.SSHKey
   :members:
   :private-members:

Size Class
----------

.. autoclass:: pontoon.lib.Size
   :members:
   :private-members:

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
