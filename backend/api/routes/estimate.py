from fastapi import APIRouter
from services.estimation_service import EstimationService
import os
from core.extractor import extract_interventions

router = APIRouter()

RULEBOOK_PATH = os.path.join("data", "rulebook.json")
service = EstimationService(RULEBOOK_PATH)


@router.post("/estimate")
def estimate(intervention: str, clause_key: str, chainage: str, chainage_m: dict):
    result = service.estimate(intervention, clause_key, chainage_m)
    print("ESTIMATION OUTPUT:", result)
    return result
    
