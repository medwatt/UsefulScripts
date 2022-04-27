#!/usr/bin/env bash

TMPFILE=$(mktemp).tex

if [[ $OSTYPE == "linux-gnu" ]]; then
    urxvt -fn "xft:Iosevka Term:pixelsize=24" -geometry 60x10 -e vim -u ~/.config/vim/vimrc -c 'startinsert' $TMPFILE
    echo "" | xclip -selection clipboard
    python3 $(dirname "$0")/latex_script.py $TMPFILE
    xdotool key Ctrl+v
fi
