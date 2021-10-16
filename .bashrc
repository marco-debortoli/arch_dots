#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='[\u@\h \W]\$ '

# User defined aliases
alias ls='ls --color=auto'
alias psa='ps --ppid 2 -p 2 --deselect'

## Aliases for note taking
alias notesyncpush="git add -u; git commit -m 'Sync made on `date`'; git push"
alias notesyncpull="git pull"

## Aliases for package management
alias yay-update="yay -Syyu"
alias yay-list="yay -Qqe"

## Aliases for Task Management
# QED all
alias tsq="task +qed list"

# Qed low priority
alias taqlp="task add +qed priority:L"
alias tsqlp="task +qed priority:L list"

# Task add qed medium priority
alias taqmp="task add +qed priority:M"
alias tsqmp="task +qed priority:M list"

# Task add qed high priority
alias taqhp="task add +qed priority:H"
alias tsqhp="task +qed priority:H list"