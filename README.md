# dotfiles

My personal dotfiles and configurations.

## Contents

- `common/` - A set of configuration files common to every system.

- `$hostname/` - Configuration files specific to the system with the given
  hostname.

- `$x/` - Additional (optional) configurations that can also be added.

- `install` - A file-copying utility script.

## Configuration

Each subdirectory in this repository is a collection of configuration files
relative to the user's home directory. For example, adding the file
`common/.config/x` will install it to `$HOME/.config/x` when the `install`
script chooses the `common` subdirectory.

Files are chosen from these subdirectories in order, with precedence given to
the subdirectory listed first if multiple have a file in the same location:

- Custom subdirectories passed by command line (from left to right).

- The subdirectory that is the same as the system's hostname.

- The `common` subdirectory.

Note that any files existing in the subdirectory will be created, but the
script cannot detect when files are removed and will not attempt to remove
anything from the home directory.

## Installation

Made easy by the `install` script.

### Requirements

- `rsync`, used as the smart file copy utility.

### Environment

- `HOME` - The home directory of the user running this script.

- `HOSTNAME` - The hostname of this system. If not present, defaults to the
  value of `hostname`.

- `DOTFILES` - The repository root. If not present, the directory containing
  the `install` script is used.

### Steps

```
# Fetch the repository (if you haven't already):
git clone git@gitlab.com:agausmann/dotfiles.git ~/.dotfiles
cd ~/.dotfiles

# Make sure submodules are up to date (thinks like third-party Vim plugins):
git submodule update --init

# Run the script:
./install [ custom_targets ... ]
```
