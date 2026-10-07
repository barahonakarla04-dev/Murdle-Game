"""
Murdle.py - START THE GAME FROM HERE.

    py Murdle.py

This is also the file that becomes Murdle.exe.

It opens the main menu, and every time a screen closes because the
player clicked to go somewhere else, it opens that next screen.
When the player closes a window with the X, the game ends.
"""

import runpy
import sys

import navigation


navigation.launcher_running = True

# Start on the main menu (or on a screen named after "py Murdle.py ...")
navigation.next_screen = sys.argv[1] if len(sys.argv) > 1 else "main"

while navigation.next_screen:

    file_to_run = navigation.SCREENS.get(navigation.next_screen, "main")

    # Clear it first. If the player closes the window with the X,
    # nothing sets a new screen, and the game ends.
    navigation.next_screen = None

    runpy.run_module(file_to_run, run_name="__main__")


def _make_sure_the_app_includes_every_screen():
    # This never runs. It only tells PyInstaller to pack these files
    # into Murdle.exe.
    import main
    import Store
    import case_001
    import case_002
