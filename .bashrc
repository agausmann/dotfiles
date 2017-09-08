#
# ~/.bashrc
# Author: Adam Gausmann
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Color aliases
alias ls='ls --color=auto'

PS1='[\u@\h \W]\$ '

export EDITOR=/usr/bin/nano
export GIT_EDITOR=$EDITOR
export SUDO_EDITOR=$EDITOR

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

eval $(thefuck --alias)

if [ -e ~/.dailyfortune ]
then
	cat ~/.dailyfortune
fi
