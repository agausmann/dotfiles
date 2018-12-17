#!/bin/sh

dotfiles_dir="${DOTFILES:-$(dirname "$(realpath "$0")")}"
hostname="${HOSTNAME:-$(hostname)}"

customs=$(
    for i in $@
    do
       echo "${dotfiles_dir}/${i}/"
    done
)

rsync -lr ${customs} "${dotfiles_dir}/${hostname}/" "${dotfiles_dir}/common/" "${HOME}"
