# backend/api/controllers/cost_controller.py
"""
Cost Controller
---------------
Bridges:
    API → Quantity Estimation → Cost Engine

Consumes:
    Quantity engine output:
    {
        "intervention": "...",
        "clause_used": "...",
        "intervention_type": "...",
        "materials": {...}
    }

Produces:
    Final BOQ cost response with:
        - material-wise cost
        - SOR item match
        - total cost
"""

from typing import Dict, Any
from fastapi import HTTPException

from services.cost_engine import calculate_costs



def compute_cost_controller(estimation_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes the quantity estimation output and returns full cost breakdown.

    estimation_output (example):
    {
        "intervention": "...",
        "clause_used": "IRC67_15_28",
        "intervention_type": "SPEED_LIMIT_SIGN",
        "params_used": {...},
        "materials": {
            "ALUMINIUM_PLATE_m2": 0.2827,
            "RETRO_SHEETING_TypeXI_m2": 0.2827,
            ...
        }
    }

    """
    print("ESTIMATION INPUT:", estimation_output)


    materials = estimation_output.get("materials", {})

    if not materials:
        return {
        "intervention": estimation_output.get("intervention"),
        "clause_used": estimation_output.get("clause_used"),
        "intervention_type": estimation_output.get("intervention_type"),
        "params_used": estimation_output.get("params_used"),
        "materials": [],
        "total_cost": 0
        }


    # Run cost calculation
    try:
        cost_data = calculate_costs(materials)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute cost: {e}")

    # Build final response
    return {
        "intervention": estimation_output.get("intervention"),
        "clause_used": estimation_output.get("clause_used"),
        "intervention_type": estimation_output.get("intervention_type"),
        "params_used": estimation_output.get("params_used"),

        "materials": cost_data["items"],
        "total_cost": cost_data["total_cost"]
    }
    
