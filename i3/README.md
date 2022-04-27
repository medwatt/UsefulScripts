# About

The default behavior of i3 is to remember a single workspaces across all
monitors. As soon as you shift focus to a workspace on another monitor, i3
forgets the last visited workspace on the previous monitor. This script
"attempts" to fix this behavior by remembering the last visited workspace on
each monitor, thus making it possible to alternate between workspaces even
after shifting focus to a different monitor.

## Installation and Usage

- Make sure that python and the package `i3ipc` are installed.

- Simply copy the script to a folder of your choice and load it when i3 starts:

    `exec_always --no-startup-id $HOME/.config/i3/scripts/workspace-script.py`

- Specify a keybinding to switch between workspaces:

    `bindsym Mod4+Tab nop mode_back_and_forth`

