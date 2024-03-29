#!/usr/bin/env python3

import argparse
import os
import shutil
import socket
import subprocess
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
    default_host_filename = args.dotfiles / 'hosts' / 'default.toml'
    host_filename = args.dotfiles / 'hosts' / '{}.toml'.format(args.hostname)

    with open(default_host_filename) as host_file:
        host_config = toml.load(host_file)

    if host_filename.exists():
        with open(host_filename) as host_file:
            host_config.update(toml.load(host_file))

    host_config['name'] = args.hostname

    # Preprocess output configs for sway 
    for input in host_config.get('inputs', []):
        # Generate config lines for sway template
        lines = []
        for key in input:
            if key == 'match':
                continue
            if isinstance(input[key], list):
                val = ' '.join(repr(elem) for elem in input[key])
            else:
                val = repr(input[key])
            lines.append(f'{key} {val}')

        input['sway-lines'] = lines

    for output in host_config['outputs']:
        # Generate config lines for sway template
        lines = []
        for key in output:
            if key == 'match':
                continue
            if isinstance(output[key], list):
                val = ' '.join(repr(elem) for elem in output[key])
            else:
                val = repr(output[key])
            lines.append(f'{key} {val}')

        output['sway-lines'] = lines

        # Attempt to resolve device names for swaylock template
        # (Workaround https://github.com/swaywm/swaylock/issues/114)
        #
        # This will only work if this is run on the target host
        # and if sway is running, but that is usually the case...
        if output['match'] != '*':
            try:
                get_outputs = subprocess.check_output(
                    ['swaymsg', '-t', 'get_outputs', '-p'],
                ).decode('utf-8')
                for line in get_outputs.splitlines():
                    # Line format: Output <device> '<match identifier>'
                    if line.startswith('Output') and output['match'] in line:
                        output['device'] = line.split()[1]
                        break        
            except subprocess.CalledProcessError:
                print('Could not contact sway to retrieve output names.')
                print('Please re-run in sway to finish configuring swaylock.')

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
