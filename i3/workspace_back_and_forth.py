#!/usr/bin/python3

from i3ipc import Connection, Event

# this is the command that must be used from i3 to make use of this script
# e.g. bindsym Mod4+Tab nop mode_workspace_back_and_forth
CMD_WORKSPACE_BACK_AND_FORTH = "nop mode_workspace_back_and_forth"
CMD_WINDOW_BACK_AND_FORTH = "nop mode_window_back_and_forth"

# this dictionary saves the previous and current workspaces of all monitors
# VISITED_WORKSPACES = { monitor_name : [previous_workspace, current_workspace] }
VISTED_WORKSPACES = {}

# this dictionary saves the last visited non-floating window per workspace
# VISITED_WINDOWS = { workspace_name : window_id }
VISTED_WINDOWS = {}

# this saves the name of the focused monitor
FOCUSED_MONITOR = ""
FOCUSED_WINDOW = ""

# this variable is set whenever there's a workspace change
WORKSPACE_CHANGE = False


def on_workspace(self, event):
    """
    This event is triggered every time there's a workspace change.
    """
    global VISTED_WORKSPACES
    global FOCUSED_MONITOR
    global WORKSPACE_CHANGE

    # update the last workspace only when we are on the same monitor
    if FOCUSED_MONITOR == event.current.ipc_data['output']:
        VISTED_WORKSPACES[FOCUSED_MONITOR] = [event.old.name, event.current.name]
        FOCUSED_MONITOR = event.current.ipc_data['output']

    # also update when we switch monitors but don't return to the focused workspaces
    else:
        FOCUSED_MONITOR = event.current.ipc_data['output']
        if event.current.name != VISTED_WORKSPACES[FOCUSED_MONITOR][1]:
            VISTED_WORKSPACES[FOCUSED_MONITOR] =[VISTED_WORKSPACES[FOCUSED_MONITOR][1] , event.current.name]

    # let everyone know that that the workspace has changed
    WORKSPACE_CHANGE = True


def on_window(self, event):
    """
    This event is triggered every time there's a change in window focus.
    """
    global FOCUSED_WINDOW
    global VISTED_WINDOWS
    global WORKSPACE_CHANGE

    current_window = event.ipc_data["container"]["id"];                 # get the id of the current window
    floating_status = event.ipc_data["container"]["floating"]           # check whether the current window is floating
    current_workspace = i3.get_tree().find_focused().workspace().name   # get the name of the current workspace

    # we should not update when we switch workspaces, otherwise executing the command
    # will switch workspaces as the last two windows are from different workspaces
    if not WORKSPACE_CHANGE:
        # we also ignore floating windows since floating windows tend to be dialog boxes, popups, etc.
        if floating_status != "user_on" and current_window != FOCUSED_WINDOW:
            VISTED_WINDOWS[current_workspace] = FOCUSED_WINDOW
            FOCUSED_WINDOW = current_window
    else:
        FOCUSED_WINDOW = current_window
        # visiting a workspace for the first time
        if current_workspace not in VISTED_WINDOWS.keys():
            VISTED_WINDOWS[current_workspace] = current_window

    # since we're in the same workspace, set this to False
    WORKSPACE_CHANGE = False

def on_binding(self, event):
    """
    This event is triggered every time a key is pressed from within i3.
    """
    # get the command called from within i3
    command = event.binding.command

    # switch workspaces if the correct command was issued
    if command == CMD_WORKSPACE_BACK_AND_FORTH:
        current_output = i3.get_tree().find_focused().ipc_data['output']
        i3.command(f"workspace {VISTED_WORKSPACES[current_output][0]}")

    elif command == CMD_WINDOW_BACK_AND_FORTH:
        current_workspace = i3.get_tree().find_focused().workspace().name
        i3.command(f"[con_id={VISTED_WINDOWS[current_workspace]}] focus")


def init():
    global FOCUSED_WINDOW
    global FOCUSED_MONITOR
    global VISTED_WORKSPACES

    # get the current focused window, workspace, and monitor
    current_focus = i3.get_tree().find_focused()
    current_workspace = current_focus.workspace().name
    FOCUSED_MONITOR = current_focus.ipc_data['output']
    FOCUSED_WINDOW = current_focus.ipc_data["id"]

    # set the former and current workspaces of all monitors to be the current ones
    # because we haven't visited any workspaces yet
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
    i3.on(Event.WINDOW_NEW, on_window)
    i3.on(Event.WINDOW_FOCUS, on_window)

    i3.main()
