"""
navigation.py - moves the player between screens.

Instead of starting a separate .py file for every screen (which stops
working inside an .exe), each screen now says "go to the store" (or
another screen), closes its window, and Murdle.py opens the next one.

Screen names you can use with go_to():
    "main", "case_001", "case_002", "store"
"""

import os
import subprocess
import sys

import pygame


# Screen name  ->  the file that runs it (without .py)
SCREENS = {
    "main": "main",
    "case_001": "case_001",
    "case_002": "case_002",
    "store": "Store",
}

# Murdle.py fills these in
next_screen = None
launcher_running = False


def go_to(root, screen_name):

    global next_screen

    # Stop this screen's music, so it doesn't keep playing on the next one
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

    next_screen = screen_name

    root.destroy()

    # If you started a single screen directly (for example
    # "py Store.py" while testing), start the game properly instead
    if not launcher_running:
        game_folder = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen([
            sys.executable,
            os.path.join(game_folder, "Murdle.py"),
            screen_name
        ])
