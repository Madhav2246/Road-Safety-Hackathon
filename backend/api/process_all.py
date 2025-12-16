# backend/api/process_all.py

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import os

from services.estimation_service import EstimationService
from services.cost_engine import calculate_costs
from services.demographics_service import DemographicsService

# ---------------------------------------------------------
# Router
# ---------------------------------------------------------
router = APIRouter(prefix="/api", tags=["Process All"])

# ---------------------------------------------------------
# Services
# ---------------------------------------------------------
RULEBOOK_PATH = os.path.join("data", "rulebook.json")
estimator = EstimationService(RULEBOOK_PATH)

# ---------------------------------------------------------
# Endpoint
# ---------------------------------------------------------
@router.post("/process-all")
def process_all(interventions: List[Dict[str, Any]]):
    """
    Full pipeline:
    1. Quantity estimation
    2. Cost estimation
    3. Analytics (demographics)

    Expected input:
    [
      {
        "intervention": "...",
        "chainage": "4+200",
        "chainage_m": { "start_m": 4200, "end_m": 4500, "length_m": 300 }
      }
    ]
    """

    results = []
    grand_total = 0.0

    for item in interventions:
        try:
            # -----------------------------
            # Quantity estimation
            # -----------------------------
            est = estimator.estimate(
                intervention=item["intervention"],
                clause_key=None,  # ⚠️ USE extracted clause, not matcher
                chainage_m=item.get("chainage_m", {})
            )

            # -----------------------------
            # Cost estimation
            # -----------------------------
            cost = calculate_costs(est.get("materials", {}),intervention_type=est.get("intervention_type"))

            results.append({
                "intervention": est.get("intervention"),
                "chainage": item.get("chainage"),
                "clause_used": est.get("clause_used"),
                "cost": cost
            })

            grand_total += cost["total_cost"]

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process intervention: {str(e)}"
            )

    # -----------------------------
    # Analytics
    # -----------------------------
    demographics = DemographicsService.compute(results)

    return {
        "interventions": results,
        "grand_total": round(grand_total, 2),
        "demographics": demographics
    }
