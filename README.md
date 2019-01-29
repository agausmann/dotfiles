# dotfiles

My personal dotfiles and configurations, generated from templates with Mako!

## Contents

- `templates/` - The set of base template files.

- `include/` - Template files that do not map directly to a generated file.

- `install.py` - The script that generates and installs the templates. (Requires Mako)

- `install` - Updates submodules and runs `pipenv run install.py "$@"`.

## How it Works

For each file in the `templates/` directory (recursively), the installation script
will parse and render it as a Mako template and output it with the same path but
relative to the home directory. Mako is configured to look for additional files in the
`include/` directory if they don't exist in `templates/`, so use that if you reference
other template files that aren't supposed to be rendered as a standalone file.

## Requirements

- Either mako (for using `install.py`) or pipenv (for `install`).

## Installation

Made easy by the `install` script. Use `install --help` to see customization options.
