# backend/api/routes/cost.py
"""
Cost API Routes
---------------
Endpoint:
    POST /cost/compute

Consumes:
    Quantity Estimation Output (JSON)

Produces:
    Final BOQ Cost Breakdown
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from api.controllers.cost_controller import compute_cost_controller

router = APIRouter(prefix="/cost", tags=["Cost Estimation"])


# ---------------------------------------------------------
# Pydantic Input Model (for validation)
# ---------------------------------------------------------
class EstimationInput(BaseModel):
    intervention: str
    clause_used: str
    intervention_type: str
    params_used: Dict[str, Any]
    materials: Dict[str, float]


# ---------------------------------------------------------
# POST /cost/compute
# ---------------------------------------------------------
@router.post("/compute")
def compute_cost_api(payload: EstimationInput):
    """
    Takes quantity estimation output and computes:
        - cost of each material
        - SOR matched item
        - total cost
    """
    estimation_dict = payload.dict()
    result = compute_cost_controller(estimation_dict)
    return result
