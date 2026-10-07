"""
save_manager.py - loads and saves the player's progress.

The save file lives in the player's own AppData folder:
    C:\\Users\\<their name>\\AppData\\Roaming\\Murdle\\save_data.json

That's the right place for an app to save things. The game's own
folder may not allow saving once the game is an .exe.

TIP: to find your save file, type  %APPDATA%\\Murdle  into the
address bar of File Explorer and press Enter.
"""

import json
import os
import sys


# What a brand new player starts with
DEFAULT_DATA = {
    "detective_money": 0,
    "case_001_solved": False,
    "case_002_solved": False,
    "purchased_items": [],
}


def save_folder():

    if sys.platform == "win32":
        base = os.getenv("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    folder = os.path.join(base, "Murdle")
    os.makedirs(folder, exist_ok=True)
    return folder


save_file = os.path.join(save_folder(), "save_data.json")


def load_data():

    try:
        with open(save_file, "r") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        # New player, or the save file got damaged: start fresh
        data = {}

    # Fill in anything missing, so older saves don't crash the game
    for key, value in DEFAULT_DATA.items():
        if key not in data:
            data[key] = list(value) if isinstance(value, list) else value

    return data


def save_data(data):

    with open(save_file, "w") as file:
        json.dump(data, file, indent=4)
