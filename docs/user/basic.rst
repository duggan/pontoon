CLI Usage
=========

Configure
---------

Set up your credentials and preferences:

::

    $ pontoon configure

You'll be prompted for your Digital Ocean API credentials (`available
here <https://www.digitalocean.com/api_access>`__), and whether you want
to use existing SSH credentials or for them to be generated (using
OpenSSH).

The rest are preferences, and can be set at any time by running
configure again, editing the ``~/.pontoon`` config file (YAML format),
or by specifying them with options on the command line.

Configuration File
------------------

Here's an example of the options set in the configuration file:

::

    api_token: foo-bar-baz 
    auth_key_name: Macbook.local
    image: ubuntu-15-10-x32
    region: lon1
    size: 512mb
    ssh_private_key: ~/.ssh/id_rsa
    ssh_public_key: ~/.ssh/id_rsa.pub
    username: root

Managing Droplets is probably what you'll spend most of your time doing with pontoon.

You can get a full list of subcommands and options by running:

::

    $ pontoon droplet --help

Basic Usage
-----------

Creating and destroying Droplets is very straight forward:

::

    $ pontoon droplet create my-droplet
    Creating Droplet my-droplet (512mb using ubuntu-15-10-x32 in lon1)...
    ...............active
    $ pontoon droplet destroy my-droplet
    Destroying ud1 and scrubbing data...

To SSH into your Droplet:

::

    $ pontoon droplet ssh my-droplet
    Welcome to Ubuntu 15.10 (GNU/Linux 4.2.0-27-generic i686)

    * Documentation:  https://help.ubuntu.com/
    Last login: Sun Mar  6 10:41:17 2016 from 192.168.1.200

To get a list of your Droplets:

::

    $ pontoon droplet list
    my-droplet:    (512mb, ubuntu-15-10-x32, lon1, 104.236.32.182, active)


See the :doc:`reference` for more.
