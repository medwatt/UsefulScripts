#!/usr/bin/python3

import math
from i3ipc import Connection, Event

class I3Tiler:

    def __init__(self, i3_connection=None):
        if not i3_connection:
            self.i3 = Connection()
        self.num_windows = 0
        self.num_columns = 1

    def __call__(self):
        # Enable dynamic tiling
        self.i3.on(Event.WINDOW_NEW, self.on_window_new)
        self.i3.on(Event.WINDOW_CLOSE, self.on_window_close)
        self.i3.on(Event.WINDOW_MOVE, self.on_window_move)

        self.i3.main()

    #######################################################################
    #                          utility functions                          #
    #######################################################################

    def get_focused_monitor(self):
        workspaces = self.i3.get_workspaces()
        try:
            if workspaces:
                focused = [w for w in workspaces if w.focused][0]
                return focused.output
        except IndexError:
            return

    def get_tree(self):
        tree = self.i3.get_tree()
        return tree

    def get_focused(self):
        tree = self.get_tree()
        focused_window = tree.find_focused()
        focused_workspace = focused_window.workspace()
        return focused_window, focused_workspace

    #######################################################################
    #                        manual-dynamic tiling                        #
    #######################################################################

    def on_window_new(self, i3, event):
        if self.num_windows <= 2:
            focused_window, workspace = self.get_focused()
            windows = [w for w in workspace.leaves() if w.window and w.floating != "user_on"]
            self.windows_num = len(windows)

            if self.windows_num == 1:
                workspace.command("split h")

            elif self.windows_num == 2:
                for i, window in enumerate(windows):
                    if i == 1:
                        window.command(f"resize set {int(workspace.rect.width * 0.4)} px")
                    window.command("split v")

    def on_window_close(self, i3, event):
        focused_window, workspace = self.get_focused()
        windows = [w for w in workspace.leaves() if w.window]
        self.windows_num = len(windows)

        # Update he number of columns the workspace has when a window is removed
        if windows:
            self.num_columns = math.floor(
                workspace.rect.width / windows[0].rect.width)

        # This logic here avoids having the situation where windows are stacked in rows
        # Note that this only works on windows close events
        if self.windows_num == 1:
            # Only one window, so split horizontally
            windows[0].command("split h")
        elif self.windows_num > 1:
            # Multiple windows, check if last window in container
            container = windows[0].parent
            if container.layout == "splitv" and container.leaves()[-1] == windows[-1]:
                # Last window in container, move first window to left and split vertically
                windows[0].command("move left")
                windows[0].command("split v")

    def on_window_move(self, i3, event):
        focused_window, workspace = self.get_focused()
        if focused_window.floating == "auto_off":
            new_num_columns = math.floor(
                workspace.rect.width / focused_window.rect.width)

            # If we move a window and it results in the creation of a new column,
            # then we should split the window vertically
            if event.container and event.container.layout == "splith":
                if new_num_columns > self.num_columns:
                    event.container.command("splitv")

            self.num_columns = new_num_columns

if __name__ == "__main__":
    main = I3Tiler()
    main()
