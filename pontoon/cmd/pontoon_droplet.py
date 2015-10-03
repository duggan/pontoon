#!/usr/bin/env python

"""Usage:
          pontoon droplet list [--detail]
          pontoon droplet create <name> [--size=<size>] [--image=<image>]
                                        [--region=<region>] [--keys=<key>...]
                                        [--private-networking]
                                        [--disable-virtio] [--no-wait]
          pontoon droplet ssh <name> [--user=<user>] [--key=<path-to-key>]
          pontoon droplet rename <from> <to>
          pontoon droplet resize <name> <size>
          pontoon droplet snapshot <droplet-name> <snapshot-name>
          pontoon droplet show <name>
          pontoon droplet status <name>
          pontoon droplet destroy <name> [--no-scrub]
          pontoon droplet start <name>
          pontoon droplet shutdown <name>
          pontoon droplet reboot <name>
          pontoon droplet restore <name> <snapshot-name>
          pontoon droplet rebuild <name> <image-name>
          pontoon droplet powercycle <name> [--yes]
          pontoon droplet poweroff <name> [--yes]
          pontoon droplet passwordreset <name> [--yes]
          pontoon droplet backups <name> [ --enable | --disable ]
          pontoon droplet field <name> <field-name>

Options:
    -h --help              Show this page.
    --detail               Show full Droplet info.
    --size=<size>          Droplet RAM allocation. [default: {size}]
    --image=<image>        Droplet image. [default: {image}]
    --region=<region>      Droplet region. [default: {region}]
    --keys=<key>...        List of registered keys to add
                           to Droplet(s) [default: {keys}].
    --private-networking   Assign private address to Droplet (where available)
    --disable-virtio       Disable VirtIO. (not recommended)
    --no-scrub             Do not perform a secure erase of the drive
                           on termination. (not recommended)
    --user=<user>          Override configured username for SSH login.
    --key=<path-to-key>    Override configured private key for SSH login.
    --yes                  Skip questions, assume any prompts will
                           be answered in the affirmative.

Quick guide:

    Some common operations:

        pontoon droplet list            A list of your droplets
        pontoon droplet create foo      Create a droplet called "foo"
                                        with default settings.
        pontoon droplet ssh foo         SSH into a droplet with the
                                        configured account and SSH key.
        pontoon droplet destroy foo     Terminate a droplet and secure
                                        erase the underlying drive.
        pontoon droplet field foo ip_address Output only the value of a
                                        specific field of the droplet. Useful
                                        use in scripting.
"""

import re
from subprocess import call
from .. import configure, ui
from .. import PontoonException, DropletException, ImageException
from .. import Command


class DropletCommand(Command):

    def list(self):
        droplet_list = self.pontoon.droplet.list()
        if len(set(d.name for d in droplet_list)) != len(droplet_list):
            ui.warning("Warning: multiple Droplets with identical "
                       "hostnames found. Actions on those Droplets "
                       "will fail until this is resolved in the web UI.")

        for machine in droplet_list:

            try:
                s = self.pontoon.size.name_from_id(machine.size_id)
                r = self.pontoon.region.name_from_id(machine.region_id)
            except PontoonException as e:
                ui.message(str(e))
                return 1

            try:
                i = self.pontoon.image.name_from_id(machine.image_id)
            except ImageException as e:
                i = "%s [could not determine image name]" % machine.image_id

            info = ui.format_droplet_info(machine, size=s, region=r, image=i)

            if self.args['--detail']:
                ui.message(machine.name)
                for k, v in info.items():
                    ui.message("   %-20s %s" % (k + ':', v))
            else:
                ui.message("%-15s (%s, %s, %s, %s, %s)" % (
                    machine.name + ':',
                    info['size'],
                    info['image'],
                    info['region'],
                    info['ip_address'],
                    info['status'],
                ))

    def create(self):
        ui.message("Creating Droplet %s "
                   "(%s using %s in %s)..." % (self.args['<name>'],
                                               self.args['--size'],
                                               self.args['--image'],
                                               self.args['--region'],
                                               ))

        if (self.args['--private-networking']
                and not re.match('^new york 2|amsterdam 2$',
                                 self.args['--region'], re.IGNORECASE)):
            ui.message("Warning: Only New York 2 and Amsterdam 2 are known "
                       "to support private networking.")
            ui.message("         We'll try to set it, but check after the "
                       "droplet is active.")

        try:
            self.pontoon.droplet.create(
                name=self.args['<name>'],
                size=self.args['--size'],
                image=self.args['--image'],
                region=self.args['--region'],
                keys=self.args['--keys'],
                private_networking=self.args['--private-networking'],
                disable_virtio=self.args['--disable-virtio'])
        except PontoonException as e:
            ui.message(str(e))
            return 1

        if not self.args['--no-wait']:
            state = 'starting'
            while state != 'active':
                state = self.pontoon.droplet.status(self.args['<name>'])
                ui.ticker()
            ui.message(state)

    def ssh(self):
        config = configure.combined()
        i = self.pontoon.droplet.show(self.args['<name>'])
        if self.args['--user']:
            username = self.args['--user']
        else:
            username = config.get('username')
        hostname = i.ip_address
        if self.args['--key']:
            auth_key = self.args['--key']
        else:
            auth_key = config.get('ssh_private_key')
        auth_key = ui.full_path(auth_key)

        options = ['ssh',
                   '-i', '%s' % auth_key,
                   '-o', 'StrictHostKeyChecking=no',
                   '-o', 'UserKnownHostsFile=/dev/null',
                   '-o', 'LogLevel=error',
                   '%s@%s' % (username, hostname)]
        return call(options)

    def rename(self):
        ui.message("Renaming from %s to %s..." % (
            self.args['<from>'], self.args['<to>']))
        self.pontoon.droplet.rename(
            self.args['<from>'], self.args['<to>'])

    def resize(self):
        ui.message("Resizing %s to %s" % (
            self.args['<name>'], self.args['<size>']))
        self.pontoon.droplet.resize(
            self.args['<name>'], self.args['<size>'])

    def snapshot(self):
        ui.message("Snapshotting %s as %s..." % (
                   self.args['<droplet-name>'], self.args['<snapshot-name>']))
        self.pontoon.droplet.snapshot(
            self.args['<droplet-name>'], self.args['<snapshot-name>'])

    def show(self):

        machine = self.pontoon.droplet.show(self.args['<name>'])
        try:
            s = self.pontoon.size.name_from_id(machine.size_id)
            r = self.pontoon.region.name_from_id(machine.region_id)
            i = self.pontoon.image.name_from_id(machine.image_id)
        except PontoonException as e:
            ui.message(str(e))
            return 1

        ui.message("%s" % self.args['<name>'])
        info = ui.format_droplet_info(machine, size=s, region=r, image=i)
        for k, v in info.items():
            ui.message("   %-20s %s" % (k + ':', v))

    def status(self):
        ui.message(self.pontoon.droplet.status(self.args['<name>']))

    def destroy(self):
        scrubbing = ""
        if not self.args['--no-scrub']:
            scrubbing = " and scrubbing data"

        ui.message("Destroying %s%s..." % (
            self.args['<name>'], scrubbing))
        self.pontoon.droplet.destroy(
            self.args['<name>'], self.args['--no-scrub'])

    def start(self):
        ui.message("Starting %s..." % self.args['<name>'])
        self.pontoon.droplet.start(self.args['<name>'])

    def shutdown(self):
        ui.message("Shutting down %s" % self.args['<name>'])
        self.pontoon.droplet.shutdown(self.args['<name>'])

    def reboot(self):
        ui.message("Rebooting %s" % self.args['<name>'])
        self.pontoon.droplet.reboot(self.args['<name>'])

    def restore(self):
        ui.message("Restoring %s from snapshot %s..." % (
                   self.args['<name>'], self.args['<snapshot-name>']))
        self.pontoon.droplet.restore(
            self.args['<name>'], self.args['<snapshot-name>'])

    def rebuild(self):
        ui.message("Rebuilding %s using %s..." % (
                   self.args['<name>'], self.args['<image-name>']))
        self.pontoon.droplet.rebuild(
            self.args['<name>'], self.args['<image-name>'])

    def powercycle(self):
        if self.args['--yes']:
            ui.message('Powercycling %s...' % self.args['<name>'])
            self.pontoon.droplet.powercycle(self.args['<name>'])
        else:
            ui.notify("Powercycling a server could cause processes not to "
                      "shut down correctly, and potentially data loss or "
                      "corruption. "
                      "The 'reboot' command is the recommended way to restart "
                      "a machine.")
            if ui.ask_yesno("Do you wish to continue?"):
                ui.message('Powercycling %s...' % self.args['<name>'])
                self.pontoon.droplet.powercycle(self.args['<name>'])

    def poweroff(self):
        if self.args['--yes']:
            ui.message('Powering off %s...' % self.args['<name>'])
            self.pontoon.droplet.poweroff(self.args['<name>'])
        else:
            ui.notify("Powering off a server could cause processes not to "
                      "shut down correctly, and potentially data loss or "
                      "corruption. The 'shutdown' command is the recommended "
                      "way to turn off a machine.")
            if ui.ask_yesno("Do you wish to continue?"):
                ui.message('Powering off %s...' % self.args['<name>'])
                self.pontoon.droplet.poweroff(self.args['<name>'])

    def passwordreset(self):
        if self.args['--yes']:
            ui.message('Resetting root password for %s...' % (
                self.args['<name>']))
            self.pontoon.droplet.passwordreset(self.args['<name>'])
            ui.message('You should receive an email shortly.')
        else:
            ui.notify("Resetting the root password requires a reboot.")
            if ui.ask_yesno("Do you want to continue?"):
                ui.message('Resetting root password for %s...' % (
                    self.args['<name>']))
                self.pontoon.droplet.passwordreset(self.args['<name>'])
                ui.message('You should receive an email shortly.')

    def backups(self):
        action = ''
        if self.args['--enable']:
            action = 'enable'
        elif self.args['--disable']:
            action = 'disable'
        else:
            ui.message("action must be either 'enable' or 'disable'")
            return 1

        ui.message("%s backups for %s..." % (action, self.args['<name>']))
        self.pontoon.droplet.backups(action, self.args['<name>'])

    def field(self):
        if '<field-name>' not in self.args:
            ui.message('Parameter "field-name" must be given')
            return 1
        machine = self.pontoon.droplet.show(self.args['<name>'])
        info = ui.format_droplet_info(machine)
        ui.message("%s" % info[self.args['<field-name>']])


if __name__ == '__main__':

    try:
        config = configure.combined()
        cmd = DropletCommand(
            str(__doc__.format(
                size=config.get('size', None),
                image=config.get('image', None),
                region=config.get('region', None),
                keys=config.get('auth_key_name', None),
                scrub=config.get('scrub_data', None))))
        exit(cmd.run())
    except PontoonException as e:
        ui.message(str(e))
        exit(1)
