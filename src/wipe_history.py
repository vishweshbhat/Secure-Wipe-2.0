import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui'))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(REPORTS_DIR, "wipe_history.json")

def save_wipe_record(record):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    history.append(record)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)

def load_wipe_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
