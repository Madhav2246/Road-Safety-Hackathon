import math
from typing import Dict, Any


class QuantityEstimator:
    """
    Supports ONLY list-style material definitions:

    "materials": [
        { "code": "ITEM_m2", "qty_formula": "(width_mm * height_mm)/1e6" },
        { "code": "MS_POST_nos", "qty_formula": "count" }
    ]
    """

    def __init__(self, rulebook_path: str):
        import json, os

        if not os.path.exists(rulebook_path):
            raise FileNotFoundError(f"Rulebook not found at {rulebook_path}")

        with open(rulebook_path, "r", encoding="utf-8") as f:
            self.rulebook = json.load(f)

    # --------------------------------------------------------------
    # SAFE FORMULA EVALUATION (CRITICAL FIX)
    # --------------------------------------------------------------
    def _eval_formula(self, formula: str, params: dict) -> float:
        try:
            # Ensure params is always a dict
            safe_locals = dict(params) if params else {}

            # Explicitly allow safe functions
            safe_locals.update({
                "math": math,
                "int": int,
                "round": round,
                "max": max,
                "min": min,
                "float": float
            })

            value = eval(
                formula,
                {"__builtins__": {}},   # no unsafe builtins
                safe_locals
            )

            return float(value)

        except Exception as e:
            print(f"[WARN] Error evaluating formula '{formula}' with params {params}: {e}")
            return 0.0

    # --------------------------------------------------------------
    # MATERIAL COMPUTATION
    # --------------------------------------------------------------
    def compute_materials(self, materials_spec, params) -> Dict[str, float]:
        results = {}

        for item in materials_spec:
            code = item["code"]
            formula = item.get("qty_formula", "0")

            qty = self._eval_formula(formula, params)
            results[code] = round(qty, 4)

        return results

    # --------------------------------------------------------------
    # PUBLIC ENTRY POINT
    # --------------------------------------------------------------
    def estimate(self, intervention_type: str, params: dict) -> Dict[str, Any]:
        if intervention_type not in self.rulebook:
            return {
                "error": f"Unknown intervention type: {intervention_type}",
                "materials": {}
            }

        rule = self.rulebook[intervention_type]

        # Merge defaults + runtime params
        context = {}
        context.update(rule.get("defaults", {}))
        context.update(params or {})

        materials = rule.get("materials", [])
        results = self.compute_materials(materials, context)

        return {
            "intervention_type": intervention_type,
            "params_used": context,
            "materials": results
        }
