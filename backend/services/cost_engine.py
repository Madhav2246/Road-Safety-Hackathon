from typing import Dict, Any
from services.price_service import find_best_sor_match
import json
import os

INSTALLATION_JSON = os.path.join("data", "installation_costs.json")


# --------------------------------------------------
# LOAD INSTALLATION COSTS
# --------------------------------------------------
def load_installation_costs() -> Dict[str, Any]:
    if not os.path.exists(INSTALLATION_JSON):
        return {}
    with open(INSTALLATION_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------
# COST CALCULATION
# --------------------------------------------------
def calculate_costs(
    materials: Dict[str, float],
    intervention_type: str | None = None
) -> Dict[str, Any]:

    items = []
    total = 0.0

    # ----------------------------------
    # 1. MATERIAL COSTS
    # ----------------------------------
    for material, qty in materials.items():
        unit = material.split("_")[-1] if "_" in material else None

        price = find_best_sor_match(material, qty, unit)
        amount = price.get("estimated_cost") or 0.0
        best = price.get("best_match") or {}

        items.append({
            "material": material,
            "qty": qty,
            "unit": unit,
            "rate": best.get("rate"),
            "amount": round(amount, 2),
            "type": "material"
        })

        total += amount

    # ----------------------------------
    # 2. INSTALLATION COST (DIRECT LOOKUP)
    # ----------------------------------
    installation_map = load_installation_costs()

    inst_rate = 0.0
    inst_unit = "job"

    if intervention_type:
        key = intervention_type.strip().upper()

        if key in installation_map:
            inst_rate = float(installation_map[key]["rate"])
            inst_unit = installation_map[key].get("unit", "job")
        else:
            print(f"⚠️ Installation cost not found for: {key}")
    else:
        print("⚠️ intervention_type is None")

    # ALWAYS ADD INSTALLATION ROW
    items.append({
        "material": "INSTALLATION_CHARGES (As per CPWD SOR)",
        "qty": 1,
        "unit": inst_unit,
        "rate": inst_rate,
        "amount": round(inst_rate, 2),
        "type": "installation"
    })

    total += inst_rate

    return {
        "items": items,
        "total_cost": round(total, 2)
    }
