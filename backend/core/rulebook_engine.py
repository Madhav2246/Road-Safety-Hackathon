# backend/core/rulebook_engine.py
import json
from typing import Dict, Any, List

class RulebookEngine:
    def __init__(self, rulebook_path: str):
        with open(rulebook_path, "r", encoding="utf-8") as f:
            self.rulebook = json.load(f)

    def compute_materials(self, intervention: Dict[str,Any]) -> Dict[str,Any]:
        """
        Minimal implementation: map intervention keywords to materials using rulebook mapping.
        rulebook.json expected to have entries like:
        { "thermoplastic": { "materials": [{"item":"THERMO_PAINT","qty_per_m":1}] }, ... }
        """
        text = (intervention.get("intervention") or "").lower()
        materials = {}
        for key, info in self.rulebook.items():
            # key might be a category or keyword
            if key.lower() in text:
                mats = info.get("materials", [])
                for m in mats:
                    name = m.get("item")
                    qty = m.get("qty_per_m", 1)
                    unit = m.get("unit", "nos")
                    # naive quantity: if chainage known, multiply; otherwise use default_quantity
                    chain = intervention.get("chainage")
                    qty_val = m.get("default_quantity", 1)
                    # override if chainage length present in a dict
                    if isinstance(chain, dict) and chain.get("length"):
                        qty_val = qty * chain.get("length")
                    materials[name] = {"quantity": qty_val, "unit": unit}
        return materials
