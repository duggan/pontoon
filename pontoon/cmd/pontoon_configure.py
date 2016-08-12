#!/usr/bin/env python

"""Usage: pontoon configure [--help]

Options:
    -h --help       Show this page.
"""

import logging
from docopt import docopt
from ..lib import Manager
from .. import configure, ui
from ..command import Command
from .. import MOCK


class ConfigureCommand(Command):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.manager = Manager(token=config['api_token'], mocked=MOCK)

    def interactive(args):
        config = {}
        default = {}
        default['ssh_private_key'] = '~/.ssh/id_rsa'
        default['ssh_public_key'] = '~/.ssh/id_rsa.pub'

        ui.heading("Configure your Digital Ocean account with pontoon.")
        current = configure.combined()

        existing_token = " (current: %s)" % ui.mask(
            current['api_token']) if current['api_token'] else ""

        api_token = ui.ask("Personal Access Token%s" % existing_token)

        if api_token:
            config['api_token'] = api_token
        else:
            config['api_token'] = current['api_token']

        if configure.ssh_tools():
            ui.notify("Pontoon can either use an existing SSH "
                      "key or generate a new one using OpenSSH "
                      "(Linux/BSD/Mac only)")
        else:
            ui.warning("Pontoon cannot find openssl, "
                       "so won't be able to create keys.")

        if ui.ask_yesno("Use an existing keypair?"):
            for key in ['private', 'public']:
                key_name = 'ssh_%s_key' % key
                auth_key = ui.ask("Path to SSH %s key (default %s)" % (
                                  key, default[key_name]))
                if auth_key:
                    config[key_name] = auth_key
                elif key_name in current and current[key_name]:
                    config[key_name] = current[key_name]
                else:
                    config[key_name] = default[key_name]

                while not ui.valid_path(config[key_name]):
                    ui.message("No key found at %s, retry?" % config[key_name])
                    config[key_name] = ui.ask("Path to SSH private key")

        else:
            for key in ['private', 'public']:
                key_name = 'ssh_%s_key' % key
                auth_key = ui.ask("Path to SSH %s key (default %s)" % (
                                  key, default[key_name]))
                if auth_key:
                    config[key_name] = auth_key
                elif key_name in current and current[key_name]:
                    config[key_name] = current[key_name]
                else:
                    config[key_name] = default[key_name]

            if ui.valid_path(
                config['ssh_private_key']) and not ui.valid_path(
                    config['ssh_public_key']):
                ui.message("Regenerating public key...")
                configure.regenerate_public_key(
                    config['ssh_private_key'], config['ssh_public_key'])

            else:
                configure.rsa_keygen(config['ssh_private_key'])

        config['auth_key_name'] = ui.machine()
        public_key = configure.read_key(config['ssh_public_key'])

        ui.message("Registering public key with name '%s'..." % (
                   config['auth_key_name']))
        try:
            configure.register_key(config,
                                   config['auth_key_name'],
                                   public_key)
            ui.message("ok!")
        except Exception as e:
            ui.message(str(e))
            pass

        for option in ['size', 'region', 'image']:
            ui.message("Choose a default %s:" % option)
            option_choices = {}
            option_index = 1
            options = getattr(configure, "%ss" % option)(config)
            for o in options:
                option_choices[option_index] = o.slug
                ui.message(" %-3s %s" % (str(option_index) + '.', o.slug))
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


def main():
    try:
        configure.logger()

        config = configure.combined()

        args = docopt(str(__doc__))

        exit(ConfigureCommand(config, args).run("interactive"))

    except Exception as e:
        ui.message(str(e))
        exit(1)

if __name__ == '__main__':
    main()
