#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

from mako.lookup import TemplateLookup

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
        help='The hostname or other identifying name of this system.',
        default=os.environ.get('HOSTNAME'),
    )
    parser.add_argument(
        '-o', '--home',
        help='The home directory where generated dotfiles will be installed.',
        default=os.environ.get('HOME') or Path.home(),
    )
    args = parser.parse_args()



main()
