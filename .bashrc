#
# ~/.bashrc
# author: adam gausmann
#


# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export EDITOR=/usr/bin/vim
export GIT_EDITOR=$EDITOR
export SUDO_EDITOR=$EDITOR

# Powerline
PS1='[\u@\h \W]\$ '

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

