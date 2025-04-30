# storage.py
import json
from pathlib import Path

CANDIDATE_FILE = Path("data/candidates.json")

def load_candidates():
    if not CANDIDATE_FILE.exists():
        return []
    with open(CANDIDATE_FILE, "r") as f:
        return json.load(f)

def save_candidate(candidate_data):
    candidates = load_candidates()
    candidates.append(candidate_data)
    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=2)
