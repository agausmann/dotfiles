# dotfiles

My personal dotfiles and configurations.

## The Contents

- `common` - A set of configuration files common to every system.
- `$hostname` - Configuration files specific to the system with the given hostname.
- `$x` - Additional (optional) configurations that can also be added.

## The System

Each subdirectory of this repository is a collection of files to install
relative to the current user's home directory (assumed to be `$HOME`)
which are merged into the home directory by the `install.sh` script.
The script chooses specific subdirectories and merges them in the following
order, with precedence given to the more recently-listed subdirectory if two or
more contain a file at the same path:

- Command-line arguments (precedence given first-to-last)
- System hostname
- The `common` directory
