#!/bin/bash

selected=$(echo "Lock
Suspend
Restart
Shutdown" | rofi -dmenu -p "Select Power Option")

if [ "$selected" == "Lock" ]; then
    betterlockscreen -l dim
	exit
fi

if [ "$selected" == "Suspend" ]; then
	systemctl suspend
    exit
fi

if [ "$selected" == "Restart" ]; then
    reboot
    exit
fi

if [ "$selected" == "Shutdown" ]; then
	shutdown now
    exit
fi
