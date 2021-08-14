#!/bin/bash

cp .config/qtile/config.py ~/.config/qtile/config.py
cp .config/qtile/key_config.py ~/.config/qtile/key_config.py

# Scripts
cp -r scripts ~/.config

find ~/.config/scripts -type f -exec chmod +x {} \;