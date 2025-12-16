"""
Price Service
-------------
Provides:
    - find_best_sor_match(material, qty, unit)
"""

from typing import Optional, Dict, Any
import pandas as pd
import re
import logging
from rapidfuzz import fuzz

__all__ = ["find_best_sor_match"]

logger = logging.getLogger("services.price_service")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

_SOR_DF = None


def load_sor_csv(path: str = "data/sor_csv/2023/roads.csv") -> pd.DataFrame:
    global _SOR_DF

    if _SOR_DF is None:
        logger.info(f"Loading SOR CSV from {path}")
        df = pd.read_csv(path)
        df.fillna("", inplace=True)
        df.columns = [c.lower().strip() for c in df.columns]

        if not {"description", "unit", "unit_rate"}.issubset(df.columns):
            raise ValueError("SOR CSV must contain description, unit, unit_rate")

        _SOR_DF = df

    return _SOR_DF


STOPWORDS = {"mm", "for", "in", "and", "of", "with"}

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s./-]", " ", text)
    return " ".join(t for t in text.split() if t not in STOPWORDS)


UNIT_EQUIVALENCE = {
    "nos": {"nos", "each", "set", ""},
    "m2": {"m2", "sqm", "sq.m", "sq.m."},
    "m": {"m", "rm"},
    "kg": {"kg"},
    "l": {"l", "ltr", "litre"},
    "m3": {"m3", "cum", "cu.m"},
}


def unit_score(material_unit, sor_unit) -> float:
    if not material_unit or not sor_unit:
        return 0.4

    if material_unit == sor_unit:
        return 1.0

    for group in UNIT_EQUIVALENCE.values():
        if material_unit in group and sor_unit in group:
            return 0.8

    return 0.0


def find_best_sor_match(material: str, qty: float, unit: Optional[str]) -> Dict[str, Any]:
    df = load_sor_csv()

    query = normalize(material)
    material_unit = unit.lower() if unit else None

    best, best_score = None, -1

    for _, row in df.iterrows():
        desc = normalize(str(row["description"]))
        sor_unit = str(row.get("unit", "")).lower()
        rate = row.get("unit_rate")

        fuzz_score = fuzz.token_set_ratio(query, desc) / 100
        u_score = unit_score(material_unit, sor_unit)
        score = 0.7 * fuzz_score + 0.3 * u_score

        if score > best_score:
            best_score = score
            best = {
                "description": row["description"],
                "unit": sor_unit,
                "rate": float(rate) if str(rate).replace(".", "", 1).isdigit() else None,
                "fuzz_score": round(fuzz_score, 3),
                "unit_score": round(u_score, 3),
                "final_score": round(score, 3),
            }

    estimated_cost = best["rate"] * qty if best and best["rate"] else None

    return {
        "material": material,
        "qty": qty,
        "unit": unit,
        "best_match": best,
        "estimated_cost": estimated_cost,
    }
