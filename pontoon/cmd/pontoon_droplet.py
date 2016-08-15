#!/usr/bin/env python

"""Usage:
          pontoon droplet list [--detail]
          pontoon droplet create <name> [--size=<size>] [--image=<image slug>]
                                        [--region=<region>] [--keys=<key>...]
                                        [--user-data=<userdata>]
                                        [--private-networking]
                                        [--disable-virtio] [--no-wait]
          pontoon droplet ssh <name> [<command>]
                                     [--user=<user>] [--key=<path-to-key>]
          pontoon droplet rename <from> <to> [--no-wait]
          pontoon droplet resize <name> <size> [--yes] [--no-wait]
          pontoon droplet snapshot <droplet-name> <snapshot-name>
                                    [--yes] [--no-wait]
          pontoon droplet show <name> [--field=<field>]
          pontoon droplet status <name>
          pontoon droplet destroy <name>
          pontoon droplet start <name> [--no-wait]
          pontoon droplet shutdown <name> [--no-wait]
          pontoon droplet reboot <name> [--no-wait]
          pontoon droplet restore <name> <snapshot-name> [--no-wait]
          pontoon droplet rebuild <name> <image-name> [--no-wait]
          pontoon droplet powercycle <name> [--yes] [--no-wait]
          pontoon droplet poweroff <name> [--yes] [--no-wait]
          pontoon droplet passwordreset <name> [--yes]
          pontoon droplet backups <name> [ --enable | --disable ]

Options:
    -h --help              Show this page.
    --detail               Show full Droplet info.
    --field=<field>        Retrieve specified field from Droplet output.
                           Access with dot notation:
                              e.g., --field=networks.v4.0.ip_address
    --size=<size>          Droplet RAM allocation. [default: {size}]
    --image=<image slug>   Droplet image slug. [default: {image}]
                           List images with: pontoon image list
    --region=<region>      Droplet region. [default: {region}]
    --keys=<key>...        List of registered keys to add
                           to Droplet(s) [default: {keys}].
    --user-data=<userdata> String of user data to pass to Droplet.
                           Include a file like: --user-data="$(cat file.yml)"
    --private-networking   Assign private address to Droplet (where available)
    --disable-virtio       Disable VirtIO. (not recommended)
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
"""

import re
from subprocess import call
from functools import reduce
from docopt import docopt
from ..lib import Manager, Droplet, SSHKey
from .. import configure, ui
from ..command import Command
from .. import MOCK


class DropletCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def _get_droplet(self, name):
        droplets = self.manager.get_all_droplets()
        droplet = [droplet for droplet in droplets if droplet.name == name]

        if len(droplet) > 1:
            ui.warning("Warning: multiple Droplets with identical "
                       "hostnames found. Actions on those Droplets "
                       "will fail until this is resolved in the web UI.")
            raise Exception("Multiple Droplets named '%s'" % name)

        if len(droplet) == 0:
            raise Exception("No Droplet named '%s'" % name)

        return droplet[0]

    def _get_image(self, name):
        resources = self.manager.get_images()
        resource = [res for res in resources if res.name == name]

        if len(resource) > 1:
            ui.warning("Warning: multiple images with identical "
                       "names found. Actions on those images "
                       "will fail until this is resolved in the web UI.")
            raise Exception("Multiple images named '%s'" % name)

        if len(resource) == 0:
            raise Exception("No image named '%s'" % name)

        return resource[0]

    def _wait(self, event, droplet, status="completed"):
        if not self.args['--no-wait']:
            state = 'in-progress'
            while state != 'completed':
                actions = droplet.get_actions()
                for action in actions:
                    if action.id == event['action']['id']:
                        state = action.status
                ui.ticker()
            ui.message(status)

    def list(self):
        droplet_list = self.manager.get_all_droplets()
        if len(set(d.name for d in droplet_list)) != len(droplet_list):
            ui.warning("Warning: multiple Droplets with identical "
                       "hostnames found. Actions on those Droplets "
                       "will fail until this is resolved in the web UI.")

        for machine in droplet_list:

            if self.args['--detail']:
                ui.message(machine.name)
                details = ui.format_droplet_info(machine)
                ui.yaml_message(details)
            else:
                ui.message("%-15s (%s, %s, %s, %s, %s)" % (
                    machine.name + ':',
                    machine.size_slug,
                    machine.image['slug'],
                    machine.region['slug'],
                    machine.ip_address,
                    machine.status,
                ))

    def create(self):
        ui.message("Creating Droplet %s "
                   "(%s using %s in %s)..." % (self.args['<name>'],
                                               self.args['--size'],
                                               self.args['--image'],
                                               self.args['--region'],
                                               ))

        try:
            if self._get_droplet(self.args['<name>']):
                ui.message("Cannot create two Droplets with same name.")
                return 1
        except Exception as e:
            pass

        try:
            droplet = Droplet(token=self.config['api_token'], mocked=MOCK)
            ssh_keys = [k.id for k in
                        self.manager.get_all_sshkeys() if k.name in
                        self.args['--keys']]

            droplet.create(
                name=self.args['<name>'],
                size=self.args['--size'],
                image=self.args['--image'],
                region=self.args['--region'],
                ssh_keys=ssh_keys,
                user_data=self.args['--user-data'],
                private_networking=self.args['--private-networking'],
                disable_virtio=self.args['--disable-virtio'])
        except Exception as e:
            ui.message(str(e))
            return 1

        if not self.args['--no-wait']:
            state = 'in-progress'
            while state != 'completed':
                actions = droplet.get_actions()
                for action in actions:
                    if action.type == 'create':
                        state = action.status
                ui.ticker()
            ui.message('active')

    def ssh(self):
        droplet = self._get_droplet(self.args['<name>'])
        if self.args['--user']:
            username = self.args['--user']
        else:
            username = self.config.get('username')
        hostname = droplet.ip_address
        if self.args['--key']:
            auth_key = self.args['--key']
        else:
            auth_key = self.config.get('ssh_private_key')
        if auth_key is not None:
            auth_key = ui.full_path(auth_key)

        command = ""
        if self.args['<command>']:
            command = self.args['<command>']

        options = ['ssh',
                   '-o', 'StrictHostKeyChecking=no',
                   '-o', 'UserKnownHostsFile=/dev/null',
                   '-o', 'LogLevel=error']
        if auth_key is not None:
            options += ['-i', '%s' % auth_key]
        options += ['%s@%s' % (username, hostname),
                    '%s' % command]

        return call(options)

    def rename(self):
        ui.message("Renaming from %s to %s..." % (
            self.args['<from>'], self.args['<to>']))
        droplet = self._get_droplet(self.args['<from>'])
        droplet.rename(self.args['<to>'])

    def resize(self):
        ui.message("Resizing %s to %s" % (
            self.args['<name>'], self.args['<size>']))
        try:
            droplet = self._get_droplet(self.args['<name>'])

            # Check whether Droplet is powered off
            if droplet.status != 'off':
                if self.args['--yes']:
                    ui.message("Shutting down Droplet...")
                    event = droplet.shutdown()
                    self._wait(event, droplet, status="off")
                else:
                    if ui.ask_yesno("Droplet must be shut down during "
                                    "this process, proceed?"):
                        ui.message("Shutting down Droplet...")
                        event = droplet.shutdown()
                        self._wait(event, droplet, status="off")
                    else:
                        return

            # Perform the resize
            ui.message("Resizing...")
            event = droplet.resize(self.args['<size>'])
            self._wait(event, droplet, status="resized")

            # Boot the Droplet on completion
            if self.args['--yes']:
                ui.message("Booting...")
                event = droplet.power_on()
                self._wait(event, droplet)
            else:
                if ui.ask_yesno("Boot Droplet?"):
                    ui.message("Booting...")
                    event = droplet.power_on()
                    self._wait(event, droplet)

        except Exception as e:
            ui.message("Failed to resize: %s" % str(e))
            return 1

    def snapshot(self):
        ui.message("Snapshotting %s as %s..." % (
                   self.args['<droplet-name>'], self.args['<snapshot-name>']))
        try:
            droplet = self._get_droplet(self.args['<droplet-name>'])

            # Check whether Droplet is powered off
            if droplet.status != 'off':
                if self.args['--yes']:
                    ui.message("Shutting down Droplet...")
                    event = droplet.shutdown()
                    self._wait(event, droplet, status="shutdown")
                else:
                    if ui.ask_yesno("Droplet must be shut down"
                                    " during this process, proceed?"):
                        ui.message("Shutting down Droplet...")
                        event = droplet.shutdown()
                        self._wait(event, droplet, status="shutdown")
                    else:
                        return

            ui.message("Beginning snapshot...")
            event = droplet.take_snapshot(self.args['<snapshot-name>'])
            self._wait(event, droplet)

            # Boot the Droplet on completion
            if self.args['--yes']:
                ui.message("Booting...")
                event = droplet.power_on()
                self._wait(event, droplet)
            else:
                if ui.ask_yesno("Boot Droplet?"):
                    ui.message("Booting...")
                    event = droplet.power_on()
                    self._wait(event, droplet)

        except Exception as e:
            ui.message("Failed to snapshot: %s" % str(e))
            return 1

    def show(self):
        droplet = self._get_droplet(self.args['<name>'])
        details = ui.format_droplet_info(droplet)

        # Uses a dot notation (foo.bar.baz) to access droplet details
        # to arbitrary depth.
        if self.args['--field']:
            fields = []
            for f in self.args['--field'].split('.'):
                if f.isdigit():
                    fields.append(int(f))
                else:
                    fields.append(f)

            try:
                result = reduce(lambda d, k: d[k], fields, details)
            except Exception as e:
                ui.message("Could not access field '%s'" % (
                           self.args['--field']))
                return 1
            if isinstance(result, dict) or isinstance(result, list):
                ui.yaml_message(result)
            else:
                ui.message(result)
        else:
            ui.message(droplet.name)
            ui.yaml_message(details)

    def status(self):
        droplet = self._get_droplet(self.args['<name>'])
        ui.message(droplet.status)

    def destroy(self):
        ui.message("Destroying %s and scrubbing data..." % self.args['<name>'])
        droplet = self._get_droplet(self.args['<name>'])
        droplet.destroy()

    def start(self):
        ui.message("Starting %s..." % self.args['<name>'])
        droplet = self._get_droplet(self.args['<name>'])
        event = droplet.power_on()
        self._wait(event, droplet, status="active")

    def shutdown(self):
        ui.message("Shutting down %s" % self.args['<name>'])
        droplet = self._get_droplet(self.args['<name>'])
        event = droplet.shutdown()
        self._wait(event, droplet, status="shutdown")

    def reboot(self):
        ui.message("Rebooting %s" % self.args['<name>'])
        droplet = self._get_droplet(self.args['<name>'])
        event = droplet.reboot()
        self._wait(event, droplet, status="rebooted")

    def restore(self):
        ui.message("Restoring %s from snapshot %s..." % (
                   self.args['<name>'], self.args['<snapshot-name>']))
        droplet = self._get_droplet(self.args['<name>'])
        image = self._get_image(self.args['<snapshot-name>'])
        event = droplet.restore(image.id)
        self._wait(event, droplet, status="restored")

    def rebuild(self):
        ui.message("Rebuilding %s using %s..." % (
                   self.args['<name>'], self.args['<image-name>']))
        droplet = self._get_droplet(self.args['<name>'])
        image = self._get_image(self.args['<image-name>'])
        event = droplet.rebuild(image.id)
        self._wait(event, droplet, status="rebuilt")

    def powercycle(self):
        droplet = self._get_droplet(self.args['<name>'])
        if self.args['--yes']:
            ui.message('Powercycling %s...' % self.args['<name>'])
            event = droplet.power_cycle()
            self._wait(event, droplet, status="powercycled")
        else:
            ui.notify("Powercycling a server could cause processes not to "
                      "shut down correctly, and potentially data loss or "
                      "corruption. "
                      "The 'reboot' command is the recommended way to restart "
                      "a machine.")
            if ui.ask_yesno("Do you wish to continue?"):
                ui.message('Powercycling %s...' % self.args['<name>'])
                event = droplet.power_cycle()
                self._wait(event, droplet, status="powercycled")

    def poweroff(self):
        droplet = self._get_droplet(self.args['<name>'])
        if self.args['--yes']:
            ui.message('Powering off %s...' % self.args['<name>'])
            event = droplet.power_off()
            self._wait(event, droplet, status="poweroff")
        else:
            ui.notify("Powering off a server could cause processes not to "
                      "shut down correctly, and potentially data loss or "
                      "corruption. The 'shutdown' command is the recommended "
                      "way to turn off a machine.")
            if ui.ask_yesno("Do you wish to continue?"):
                ui.message('Powering off %s...' % self.args['<name>'])
                event = droplet.power_off()
                self._wait(event, droplet, status="poweroff")

    def passwordreset(self):
        droplet = self._get_droplet(self.args['<name>'])
        if self.args['--yes']:
            ui.message('Resetting root password for %s...' % (
                self.args['<name>']))
            event = droplet.reset_root_password()
            self._wait(event, droplet, status="reset")
            ui.message('You should receive an email shortly.')
        else:
            ui.notify("Resetting the root password requires a reboot.")
            if ui.ask_yesno("Do you want to continue?"):
                ui.message('Resetting root password for %s...' % (
                    self.args['<name>']))
                event = droplet.reset_root_password()
                self._wait(event, droplet, status="reset")
                ui.message('You should receive an email shortly.')

    def backups(self):
        action = ''
        if self.args['--enable']:
            ui.message("This action is no longer supported and will be "
                       "removed in future versions. Backups must be enabled "
                       "at Droplet creation time.")
            return 1
        elif self.args['--disable']:
            action = 'disable'
        else:
            ui.message("action must be either 'enable' or 'disable'")
            return 1

        ui.message("%s backups for %s..." % (action, self.args['<name>']))
        droplet = self._get_droplet(self.args['<name>'])
        event = droplet.disable_backups()
        self._wait(event, droplet, status="disabled")


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__.format(
            size=config.get('size', None),
            image=config.get('image', None),
            region=config.get('region', None),
            keys=config.get('auth_key_name', None))))

        exit(DropletCommand(config, args).run())

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
