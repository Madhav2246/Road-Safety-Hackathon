import json
import re
from difflib import SequenceMatcher

class ClauseMatcher:
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Your JSON is a dict:  { "clause_id": {clause_obj}, ... }
        self.clauses = []

        for cid, info in data.items():
            text = info.get("text", "").strip()
            if not text:
                continue

            self.clauses.append({
                "clause_key": cid,
                "text": text,
                "raw": info.get("_clause_raw", text),
                "source_doc": info.get("_source_doc"),
                "material_item_keyword": info.get("material_item_keyword", None),
                "default_unit": info.get("default_unit", None),
                "default_quantity": info.get("default_quantity", None),
            })

    def find_best_clause(self, intervention_text):
        """
        Returns: (clause_key, clause_data, similarity_score)
        """
        best_score = 0
        best_clause = None

        for c in self.clauses:
            score = SequenceMatcher(None, intervention_text.lower(), c["text"].lower()).ratio()
            if score > best_score:
                best_score = score
                best_clause = c

        if best_clause is None:
            return None, {"text": "", "clause_key": None}, 0.0

        return best_clause["clause_key"], best_clause, best_score
