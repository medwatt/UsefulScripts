#!/usr/bin/python3

from i3ipc import Connection, Event

# this is the command that must be used from i3 to make use of this script
# e.g. bindsym Mod4+Tab nop mode_back_and_forth
CMD_BACK_AND_FORTH = "nop mode_back_and_forth"

# this dictionary saves the previous and current workspaces of all monitors
# VISITED_WORKSPACES = { monitor_name : [previous_workspace, current_workspace] }
VISTED_WORKSPACES = {}

# this saves the name of the focused monitor
FOCUSED_MONITOR = ""


def on_workspace(self, event):
    """
    This event is triggered every time there's a workspace change
    """
    global VISTED_WORKSPACES
    global FOCUSED_MONITOR

    # update the last workspace only when we are on the same monitor
    if FOCUSED_MONITOR == event.current.ipc_data['output']:
        VISTED_WORKSPACES[FOCUSED_MONITOR] = [event.old.name, event.current.name]
        FOCUSED_MONITOR = event.current.ipc_data['output']

    # also update when we switch monitors but don't return to the focused workspaces
    else:
        FOCUSED_MONITOR = event.current.ipc_data['output']
        if event.current.name != VISTED_WORKSPACES[FOCUSED_MONITOR][1]:
            VISTED_WORKSPACES[FOCUSED_MONITOR] =[VISTED_WORKSPACES[FOCUSED_MONITOR][1] , event.current.name]


def on_binding(self, event):
    """
    This event is triggered every time there's a key pressed from within i3
    """
    # get the command called from within i3
    command = event.binding.command

    # switch workspaces if the correct command was issued
    if command.startswith(CMD_BACK_AND_FORTH):
        current_output = i3.get_tree().find_focused().ipc_data['output']
        i3.command(f"workspace {VISTED_WORKSPACES[current_output][0]}")


def init():
    global FOCUSED_MONITOR
    global VISTED_WORKSPACES

    # get the current focused workspace and focused monitor
    current_focus = i3.get_tree().find_focused()
    current_workspace = current_focus.workspace().name
    FOCUSED_MONITOR = current_focus.ipc_data['output']

    # set the former and current workspaces of all monitors to be the current ones
    # because we don't know anything yet
    for monitor in i3.get_outputs():
        VISTED_WORKSPACES[monitor.name] = [current_workspace, current_workspace]

if __name__ == "__main__":

    # connect to i3
    i3 = Connection()

    # initialize variables
    init()

    # subscribe to events
    i3.on(Event.BINDING, on_binding)
    i3.on(Event.WORKSPACE_FOCUS, on_workspace)

    i3.main()