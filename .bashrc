#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

#Colors
alias ls='ls --color=auto'

PS1='[\u@\h \W]\$ '

EDITOR=/usr/bin/nano
GIT_EDITOR=$EDITOR
SUDO_EDITOR=$EDITOR
#PATH=$PATH:/home/adam/bin

alias se="sudoedit"
alias ed=$EDITOR
alias sc="sudo systemctl"
alias screenshot="clear && screenfetch -s"
