#
# ~/.bashrc
# Author: Adam Gausmann
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export EDITOR=/usr/bin/nano
export GIT_EDITOR=$EDITOR
export SUDO_EDITOR=$EDITOR

# Powerline
if [ -z $ENABLE_POWERLINE ]
then
    PS1='[\u@\h \W]\$ '
else
    powerline-daemon -q
    POWERLINE_BASH_CONTINUATION=1
    POWERLINE_BASH_SELECT=1
    . ~/.local/lib/powerline/bindings/bash/powerline.sh
fi

# Color aliases
alias ls='ls --color=auto'

# Aliases
alias ll="ls -l"
alias la="ls -la"
alias se="sudoedit"
alias ed=$EDITOR
alias ssc="sudo systemctl"
alias snc="sudo netctl"
alias ssu="sudo su"
alias termbin="nc termbin.com 9999"
alias sloop="while true; do sl; done"

