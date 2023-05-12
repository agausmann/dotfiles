#!/usr/bin/env python3

import argparse
import os
import shutil
import socket
import sys
from functools import partial
from pathlib import Path
from typing import List

import mako.lookup
import mako.template
import requests
import toml
import yaml

BASE16_TEMPLATES_URL = 'https://raw.githubusercontent.com/chriskempson/base16-templates-source/master/list.yaml'
BASE16_TEMPLATES = yaml.safe_load(requests.get(BASE16_TEMPLATES_URL).text)

# Pending https://github.com/chriskempson/base16-templates-source/pull/106
BASE16_TEMPLATES['wofi-colors'] = 'https://github.com/agausmann/base16-wofi-colors'


def get_base16(scheme, app, template='default'):
    base_url = BASE16_TEMPLATES[app]
    if 'github.com' in base_url:
        base_url = base_url.replace('github.com', 'raw.githubusercontent.com') + '/master/'
    else:
        base_url += '/blob/master/'
    config = yaml.safe_load(requests.get(base_url + 'templates/config.yaml').text)
    output = config[template]['output']
    extension = config[template]['extension']
    return requests.get(base_url + output + '/base16-' + scheme + extension).text


def is_outdated(src: List[Path], dst: Path) -> bool:
    if not dst.exists():
        return True

    dst_modified = dst.stat().st_mtime
    return any(
        a_src.stat().st_mtime > dst_modified
        for a_src in src
        if a_src.exists()
    )


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
    parser.add_argument(
        '-f', '--force',
        help='Force overwrite all files even if they are not considered outdated.',
        action='store_true'
    )
    args = parser.parse_args()

    raw_dir = args.dotfiles / 'raw'
    templates_dir = args.dotfiles / 'templates'
    include_dir = args.dotfiles / 'include'
    host_filename = args.dotfiles / 'hosts' / '{}.toml'.format(args.hostname)

    if host_filename.exists():
        with open(host_filename) as host_file:
            host_config = toml.load(host_file)
    else:
        host_config = {}
    host_config['name'] = args.hostname

    lookup = mako.lookup.TemplateLookup(
        directories=[
            str(templates_dir),
            str(include_dir),
        ],
    )

    for raw_path in raw_dir.glob('**/*'):
        if not raw_path.is_file():
            continue
        rel_path = raw_path.relative_to(raw_dir)
        output_path = args.home / rel_path

        if args.force or is_outdated([raw_path], output_path):
            print(rel_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(raw_path, output_path)

    for template_path in templates_dir.glob('**/*'):
        if not template_path.is_file():
            continue
        rel_path = template_path.relative_to(templates_dir)
        output_path = args.home / template_path.relative_to(templates_dir)

        if args.force or is_outdated([template_path, host_filename], output_path):
            print(rel_path)
            template = mako.template.Template(
                filename=str(template_path),
                strict_undefined=True,
                lookup=lookup,
            )
            output = template.render(
                host=host_config,
                home=args.home,
                get_base16=partial(get_base16, host_config.get('base16-scheme', 'default-dark')),
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w+') as output_file:
                output_file.write(output)

            # Copy permissions from original file
            output_path.chmod(template_path.stat().st_mode & 0o777)


if __name__ == '__main__':
    main()
