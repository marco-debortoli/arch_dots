#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='[\u@\h \W]\$ '

# User defined aliases
alias ls='ls --color=auto'
alias psa='ps --ppid 2 -p 2 --deselect'
