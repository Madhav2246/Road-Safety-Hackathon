import json
import difflib
import os

class ClauseMatcher:

    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.clauses = json.load(f)

    def find_best(self, text):
        best_key = None
        best_score = 0
        best_clause = None

        for key, obj in self.clauses.items():
            ctext = obj.get("text", "")
            score = difflib.SequenceMatcher(None, text.lower(), ctext.lower()).ratio()
            if score > best_score:
                best_score = score
                best_key = key
                best_clause = obj

        return best_key, best_clause, best_score
