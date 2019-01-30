#!/usr/bin/env python3

import argparse
import os
import socket
import sys
from pathlib import Path

import mako.lookup
import mako.template
import toml


def main():
    parser = argparse.ArgumentParser(
        description='Generates and installs dotfiles for this host.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-d', '--dotfiles',
        help='The base directory of the dotfiles repository.',
        type=Path,
        default=Path(sys.argv[0]).parent,
    )
    parser.add_argument(
        '-n', '--hostname',
        help='The hostname or other identifying name of this system that will'
             ' be used to retrieve the host-specific configuration.',
        default=os.environ.get('HOSTNAME') or socket.gethostname(),
    )
    parser.add_argument(
        '-o', '--home',
        help='The home directory where generated dotfiles will be installed.',
        type=Path,
        default=os.environ.get('HOME') or Path.home(),
    )
    args = parser.parse_args()

    templates_dir = args.dotfiles / 'templates'
    include_dir = args.dotfiles / 'include'

    with open(args.dotfiles / 'hosts.toml') as hosts_file:
        hosts_config = toml.load(hosts_file)

    lookup = mako.lookup.TemplateLookup(
        directories=[
            str(templates_dir),
            str(include_dir),
        ],
    )

    for template_path in templates_dir.glob('**/*'):
        if not template_path.is_file():
            continue
        template = mako.template.Template(
            filename=str(template_path),
            strict_undefined=True,
            lookup=lookup,
        )
        output = template.render(
            host=hosts_config[args.hostname]
        )
        output_path = args.home / template_path.relative_to(templates_dir)
        with open(output_path, 'w+') as output_file:
            output_file.write(output)


main()
