Command Reference
=================

A complete list of commands and their options.

Available on the command line by appending ``--help`` to the command.

Configure
---------

The ``configure`` command interactively configures pontoon.

You're prompted for details and a configuration file is written to ``~/.pontoon``.

Alternatively, you can manually place a config file at this location with this syntax:

::

    api_token: foo-bar-baz 
    auth_key_name: Macbook.local
    image: ubuntu-15-10-x32
    region: lon1
    size: 512mb
    ssh_private_key: ~/.ssh/id_rsa
    ssh_public_key: ~/.ssh/id_rsa.pub
    username: root


.. program:: pontoon configure

.. option:: pontoon configure

   Launch interactive configuration of pontoon.

Droplets
--------


.. program:: pontoon droplet list

.. option::  pontoon droplet list [options]

.. option:: --detail

   Show full Droplet info.

::

  $ pontoon droplet list --detail
  example.com
  id: 3164444
  size: 512mb
  image: ubuntu-14-04-x64
  region: nyc3
  ip_address: 104.236.32.182
  status: active
  kernel:
     id: 2233
     name: Ubuntu 14.04 x64 vmlinuz-3.13.0-37-generic
     version: 3.13.0-37-generic
  ...

|

.. program:: pontoon droplet create

.. option:: pontoon droplet create <name> [options]

.. option:: --size size

   Droplet RAM allocation. e.g., 512mb

.. option:: --image image

   Droplet image.

.. option:: --region region

   Droplet region.

.. option:: --keys keys...

   List of registered keys to add to Droplet(s)

.. option:: --user-data userdata

   String of user data to pass to Droplet.
   Include a file like: ``--user-data="$(cat file.yml)"``

.. option:: --private-networking

   Assign private address to Droplet (where available)

.. option:: --disable-virtio

   Disable VirtIO. (not recommended)

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet ssh

.. option:: pontoon droplet ssh <name> [command] [options]

.. option:: --user user

   Override configured username for SSH login.

.. option:: --key path

   Override configured private key for SSH login.

|

.. program:: pontoon droplet rename

.. option:: pontoon droplet rename <from> <to> [options]

   Rename a Droplet. Takes the current name as the first parameter,
   and the new name as the second.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet resize

.. option:: pontoon droplet resize <name> <size> [options]

   Resize a Droplet. Takes Droplet name as first paramter, size as second.

.. option:: --yes

   Don't prompt for confirmation.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet snapshot

.. option:: pontoon droplet snapshot <droplet> <snapshot> [options]

   Snapshot a Droplet. Takes Droplet name as first paramter, snapshot name as second.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet show

.. option:: pontoon droplet show <name> [options]

   Resize a Droplet. Takes Droplet name as first paramter, size as second.

.. option:: --field field

   Extract and return a single field. Access nested items with dot syntax, e.g.:
   ``networks.v4.0.gateway``

|

.. program:: pontoon droplet status

.. option:: pontoon droplet status <name>

   Return Droplet status.

|

.. program:: pontoon droplet destroy

.. option:: pontoon droplet destroy <name>

   Destroy a Droplet.

|

.. program:: pontoon droplet start

.. option:: pontoon droplet start <name>

   Start a Droplet.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet shutdown 

.. option:: pontoon droplet shutdown <name>

   Shut down a Droplet.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet reboot

.. option:: pontoon droplet reboot <name>

   Reboot a Droplet (sending signal to OS).

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet restore

.. option:: pontoon droplet restore <name> <snapshot>

   Restore a Droplet from a snapshot.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet rebuild

.. option:: pontoon droplet rebuild <name> <image>

   Rebuild a Droplet from a given image.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet powercycle 

.. option:: pontoon droplet powercycle <name>

   Powercycle (hard restart) a Droplet.

.. option:: --yes

   Don't prompt for confirmation.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet poweroff

.. option:: pontoon droplet poweroff <name>

   Power off (without signalling the OS) a Droplet.

.. option:: --yes

   Don't prompt for confirmation.

.. option:: --no-wait

   Don't wait for action to complete, return immediately.

|

.. program:: pontoon droplet passwordreset

.. option:: pontoon droplet passwordreset <name>

   Reset the root password on a Droplet.

.. option:: --yes

   Don't prompt for confirmation.

|

.. program:: pontoon droplet backups

.. option:: pontoon droplet backups <name>

   Manage backups on a Droplet.

.. option:: --enable

   Enable backups.

.. option:: --disable

   Depracated by Digital Ocean for their v2 API release,
   later added back but still deprecated here for the moment.


Events
------

These is an interface to Digital Ocean events.

Events are usually only an implementation detail, and an interface is provided here only for completeness.

.. program:: pontoon event show

.. option:: pontoon event show <id>

   Retrieve details for a particular event id.


Images
------

Public base images made available by Digital Ocean.

.. program:: pontoon image list

.. option:: pontoon image list [options]

   Retrieve a list of public images.

.. option:: --with-ids

   Include image IDs in tabular output.

|

.. program:: pontoon image oses

.. option:: pontoon image oses

   Retrive a list of Operating Systems for which there are base images.

|

.. program:: pontoon image show

.. option:: pontoon image show <name>

   Show details for a particular image, including regions where it is available.


Regions
-------

Regions available to launch Droplets.

.. program:: pontoon region list

.. option:: pontoon region list

   List regions in which Droplets can be launched.


Sizes
-------

Droplet sizes available.

.. program:: pontoon size list

.. option:: pontoon size list

   List sizes of Droplets which can be launched.


Snapshots
---------

Commands for interacting with snapshots.

.. program:: pontoon snapshot list

.. option:: pontoon snapshot list [options]

   List available snapshots.

.. option:: --with-ids

   Include image IDs in tabular output.

|

.. program:: pontoon snapshot show

.. option:: pontoon snapshot show <name>

   Show snapshot details.

|

.. program:: pontoon snapshot destroy

.. option:: pontoon snapshot destroy <name>

   Destroy a snapshot.

|

.. program:: pontoon snapshot transfer

.. option:: pontoon snapshot transfer <name> <region>

   Move a snapshot from one region to another.
   A list of regions can be retrieved with ``pontoon region list``


SSH Keys
--------

Manage SSH keys in your account.


.. program:: pontoon sshkey list

.. option:: pontoon sshkey list

   List of SSH keys in account.

|

.. program:: pontoon sshkey add

.. option:: pontoon sshkey add <name> <public-key-path>

   Register a *public* SSH key from the specified path to your account.

|

.. program:: pontoon sshkey show

.. option:: pontoon sshkey show <name>

   Retrive a public key by name.

|

.. program:: pontoon sshkey replace

.. option:: pontoon sshkey replace <name> <public-key-path>

   Replace an existing key name with a new *public* key.


.. program:: pontoon sshkey destroy

.. option:: pontoon sshkey destroy <name>

   Remove a given key from Digital Ocean.
   Note: this doesn't remove the key from any existing Droplets, just removes
   it from the keys available to boot Droplets with.

