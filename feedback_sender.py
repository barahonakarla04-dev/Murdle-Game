"""
feedback_sender.py - sends player feedback to a Google Form (which fills a
Google Sheet for you), with an offline queue so nothing is lost.

Already set up for your "Murdle Feedback" Google Form, which has two
short answer questions: Rating and Comment.

To see the feedback: open the form, click the "Responses" tab, and
(optionally) click "Link to Sheets" to get a live spreadsheet.

Requires:  pip install requests
"""

import json
import os
import platform
import queue
import sys
import threading
import uuid
from datetime import datetime, timezone

import requests

GAME_VERSION = "1.0.0"

FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeCDZcSp0Baa4RJ9Z2adZv6bDDAaqaLbJn3h2ioSMRgpUZhkA"
    "/formResponse"
)

# Each question on your form has a hidden code. These match your form.
FIELDS = {
    "rating":  "entry.417512492",
    "comment": "entry.578340781",
}


# ============================================================
# WHERE TO STORE THINGS ON THE PLAYER'S COMPUTER
# (never inside the app bundle - that folder is read-only or
#  temporary once packaged with PyInstaller)
# ============================================================

def user_data_dir():
    if sys.platform == "win32":
        base = os.getenv("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    path = os.path.join(base, "Murdle")
    os.makedirs(path, exist_ok=True)
    return path


PENDING_FILE = os.path.join(user_data_dir(), "pending_feedback.json")
PLAYER_ID_FILE = os.path.join(user_data_dir(), "player_id.txt")

_file_lock = threading.Lock()


def get_player_id():
    """Anonymous random ID so you can tell if one player sent 10 reviews."""
    if os.path.exists(PLAYER_ID_FILE):
        with open(PLAYER_ID_FILE) as f:
            return f.read().strip()

    new_id = uuid.uuid4().hex[:12]
    with open(PLAYER_ID_FILE, "w") as f:
        f.write(new_id)
    return new_id


def _load_pending():
    try:
        with open(PENDING_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_pending(items):
    with open(PENDING_FILE, "w") as f:
        json.dump(items, f, indent=2)


def _post(entry):
    data = {FIELDS[key]: str(entry.get(key, "")) for key in FIELDS}
    response = requests.post(FORM_URL, data=data, timeout=8)
    return response.ok


def _send_all(new_entry=None):
    """Try to send everything waiting in the queue (plus a new entry).
    Returns True if the new entry got through."""
    with _file_lock:
        pending = _load_pending()
        if new_entry:
            pending.append(new_entry)

        still_waiting = []
        for item in pending:
            try:
                ok = _post(item)
            except requests.RequestException:
                ok = False
            if not ok:
                still_waiting.append(item)

        _save_pending(still_waiting)

    return new_entry is not None and new_entry not in still_waiting


# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def send_feedback(rating, comment, case="main_menu"):
    """Send in the background. Returns a Queue that will receive
    True (sent) or False (saved offline, will retry next launch)."""
    entry = {
        "rating": rating,
        "comment": comment.strip(),
        "case": case,
        "version": GAME_VERSION,
        "os": f"{platform.system()} {platform.release()}",
        "player_id": get_player_id(),
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    result = queue.Queue()
    threading.Thread(
        target=lambda: result.put(_send_all(entry)),
        daemon=True,
    ).start()
    return result


def flush_pending():
    """Call once at startup to resend anything saved while offline."""
    threading.Thread(target=_send_all, daemon=True).start()
