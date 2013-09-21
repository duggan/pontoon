.. pontoon documentation master file, created by
   sphinx-quickstart on Mon Dec  9 22:08:52 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

**Names are unique.**

Unique names make for a much easier command line experience. For
Droplets, names are hostnames, and hostnames should be unique anyway;
it's just a good idea.

They don't have to be unique *forever* though; once a Droplet is
destroyed, it's fine to use the name again.

Anything "recommended" (like secure-erasing the drive on termination) is
optional, but enabled by default.

User Guide
----------

.. toctree::
   :maxdepth: 1

   user/install
   user/library
   user/cli

API Documentation
-----------------

.. toctree::
   :maxdepth: 1

   api

Contributor Guide
-----------------

.. toctree::
   :maxdepth: 1

   dev/testing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

