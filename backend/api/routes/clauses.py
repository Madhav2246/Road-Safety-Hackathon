# backend/api/routes/clauses.py
from fastapi import APIRouter

from core.clause_matcher import ClauseMatcher

matcher = ClauseMatcher("data/irc_clauses.json")
router = APIRouter()

@router.post("/match")
def match_clause(payload: dict):
    intervention_text = payload["intervention"]
    key, clause, score = matcher.find_best(intervention_text)

    return {
        "key": key,
        "similarity": score,
        "clause": clause
    }
