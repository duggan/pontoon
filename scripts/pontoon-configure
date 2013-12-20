#!/usr/bin/env python

"""Usage: pontoon configure [--help]

Options:
    -h --help       Show this page.
"""

import logging
from pontoon import configure, ui
from pontoon import Command
from pontoon import ConfigureException


class ConfigureCommand(Command):

    def interactive(args):
        config = {}
        default = {}
        default['ssh_private_key'] = '~/.ssh/pontoon'
        default['ssh_public_key'] = '~/.ssh/pontoon.pub'

        ui.heading("Configure your Digital Ocean account with pontoon.")
        current = configure.combined()

        existing_client_id = " (current: %s)" % ui.mask(
            current['client_id']) if current['client_id'] else ""
        existing_api_key = " (current: %s)" % ui.mask(
            current['api_key']) if current['api_key'] else ""

        client_id = ui.ask("Client ID%s" % existing_client_id)
        api_key = ui.ask("API key%s" % existing_api_key)

        if client_id:
            config['client_id'] = client_id
        else:
            config['client_id'] = current['client_id']

        if api_key:
            config['api_key'] = api_key
        else:
            config['api_key'] = current['api_key']

        if configure.ssh_tools():
            ui.notify("Pontoon can either use an existing SSH "
                      "key or generate a new one using OpenSSH.")
        else:
            ui.warning("Pontoon cannot find openssl, "
                       "so won't be able to create keys.")

        if ui.ask_yesno("Use an existing keypair?"):
            for key in ['private', 'public']:
                key_name = 'ssh_%s_key' % key
                auth_key = ui.ask("Path to SSH %s key" % key)
                if auth_key:
                    config[key_name] = auth_key
                elif current[key_name]:
                    config[key_name] = current[key_name]
                else:
                    config[key_name] = default[key_name]

                while not ui.valid_path(config[key_name]):
                    ui.message("No key found at %s, retry?" % config[key_name])
                    config[key_name] = ui.ask("Path to SSH private key")

        else:
            config['ssh_private_key'] = default['ssh_private_key']
            config['ssh_public_key'] = default['ssh_public_key']

            if ui.valid_path(
                config['ssh_private_key']) and ui.valid_path(
                    config['ssh_public_key']):
                ui.message("Existing keypair found, using those.")

            elif ui.valid_path(
                config['ssh_private_key']) and not ui.valid_path(
                    config['ssh_public_key']):
                ui.message("Regenerating public key...")
                configure.regenerate_public_key(
                    config['ssh_private_key'], config['ssh_public_key'])

            else:
                configure.rsa_keygen(config['ssh_private_key'])

        config['auth_key_name'] = ui.filename_from_path(
            config['ssh_private_key'])
        public_key = configure.read_key(config['ssh_public_key'])

        ui.message("Registering public key to Digital Ocean...")
        if len([k.name for k in configure.list_keys(
               config) if k.name == config['auth_key_name']]) == 0:

            configure.register_key(config,
                                   config['auth_key_name'],
                                   public_key)
            ui.message("ok!")
        else:
            ui.message("Already registered, moving on...")

        for option in ['size', 'region', 'image']:
            ui.message("Choose a default %s:" % option)
            option_choices = {}
            option_index = 1
            options = getattr(configure, "%ss" % option)(config)
            for o in options:
                option_choices[option_index] = o.name
                ui.message(" %-3s %s" % (str(option_index) + '.', o.name))
                option_index += 1
            selection = ui.ask("%s (1-%d)" % (option.title(),
                                              len(option_choices)))
            selection = int(selection) if selection.isdigit() else 0
            while selection not in option_choices.keys():
                selection = ui.ask("Invalid selection. Choose 1-%d" % (
                    len(option_choices)))
                selection = int(selection) if selection.isdigit() else 0
            config[option] = str(option_choices[selection])

        other = {}
        for k, v in configure.defaults.items():
            val = current[k] if k in current else v['value']
            other[k] = ui.ask("%s? (currently '%s')" % (v['title'], val))

        for k, v in other.items():
            config[k] = v if v else configure.defaults[k]['value']

        configure.create_config(config)

        return 0


if __name__ == '__main__':

    try:
        cmd = ConfigureCommand(str(__doc__))
        exit(cmd.run("interactive"))
    except ConfigureException as e:
        ui.message(str(e))
        exit(1)

    exit(0)
