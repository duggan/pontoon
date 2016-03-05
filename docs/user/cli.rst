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

Create your first Droplet!
--------------------------

Now you can create your first droplet:

::

    $ pontoon droplet create foobar
    Creating Droplet foobar (512MB using Ubuntu 12.04 x64 in Amsterdam 1)...
    .......active

SSH into your Droplet
---------------------

If everything's configured correctly, you should be able to SSH into
your Droplet like so:

::

    $ pontoon droplet ssh foobar
    Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-virtual x86_64)

     * Documentation:  https://help.ubuntu.com/
    Last login: Fri May  3 18:23:56 2013
    root@foobar:~#

List your Droplets
------------------

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

Configuration file
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
