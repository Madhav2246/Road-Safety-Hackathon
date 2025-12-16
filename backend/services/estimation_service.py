# backend/services/estimation_service.py

from typing import Dict, Any
from services.quantity_estimator import QuantityEstimator
import re

class EstimationService:
    """
    Handles:
      - interpreting intervention text
      - determining intervention type
      - preparing parameters
      - calling quantity estimator
      - formatting response
    """

    def __init__(self, rulebook_path: str):
        self.qe = QuantityEstimator(rulebook_path)

    # ------------------------------------------------------------------
    # 1. CLASSIFY INTERVENTION TYPE
    # ------------------------------------------------------------------
    def classify_intervention(self, text: str) -> str:
        t = text.lower()

        # -------- SPEED / REGULATORY SIGNS --------
        if "speed" in t and ("limit" in t or "maximum" in t):
            return "SPEED_LIMIT_SIGN"

        if "no parking" in t:
            return "REGULATORY_SIGN_NOPARK"

        # -------- PEDESTRIAN SIGN (NOT MARKING) --------
        if "pedestrian" in t and "sign" in t:
            return "INFORMATORY_SIGN"

        # Zebra crossing repaint (must come FIRST)
        if "pedestrian" in t and ("crossing" in t or "zebra" in t):
            return "ZEBRA_CROSSING"

# Generic repaint AFTER that
        if "marking" in t or "repaint" in t or "painted" in t:
            return "ROAD_MARKING"

        # -------- SCHOOL AHEAD --------
        if ("school" in t or "children" in t or "side") and "ahead" in t:
            return "SCHOOL_AHEAD_SIGN"

        # -------- INFORMATORY SIGNS --------
        if any(word in t for word in ["fuel", "pump", "hospital", "parking", "petrol"]):
            return "INFORMATORY_SIGN"

        # -------- ROAD STUDS --------
        if "stud" in t or "rpm" in t or "cat eye" in t:
            return "ROAD_STUDS"

        # -------- DELINEATORS --------
        if "delineator" in t or "guide pole" in t:
            return "DELINEATOR"

        # -------- POTHOLES --------
        if "pothole" in t or "patch" in t:
            return "POTHOLE_REPAIR"

        # -------- SOLAR BLINKER --------
        if "solar blinker" in t:
            return "SOLAR_BLINKER"

        # -------- STREET LIGHT --------
        if "street light" in t or "streetlight" in t:
            return "STREET_LIGHT"
        
        if "FMM" in t or "fmm" in t:
            return "FLEXIBLE_MEDIAN_MARKER"
        


        return None

    # ------------------------------------------------------------------
    # 2. COMPUTE LENGTH FROM CHAINAGE
    # ------------------------------------------------------------------
    def compute_length_from_chainage(self, chainage: dict) -> float:
        """
        Supports:
          - start + end chainage
          - single chainage point (default 10 m)
        """
        start = chainage.get("start_m")
        end = chainage.get("end_m")

        if start is not None and end is not None and end > start:
            return end - start

        # Single chainage → assume minimum working length
        return 10.0

    # ------------------------------------------------------------------
    # 3. PREPARE PARAMETERS
    # ------------------------------------------------------------------
    def prepare_params(self, intervention_type: str, chainage_m: dict) -> dict:
        params = {}

        length_m = self.compute_length_from_chainage(chainage_m)
        params["length_m"] = length_m

        # ---------------- SIGNS ----------------
        if intervention_type in [
            "SPEED_LIMIT_SIGN",
            "SCHOOL_AHEAD_SIGN",
            "INFORMATORY_SIGN",
            "REGULATORY_SIGN_NOPARK"
        ]:
            params["count"] = 1

        # ---------------- ROAD MARKING ----------------
        elif intervention_type == "ROAD_MARKING":
            params["length_m"] = length_m
            params["width_mm"] = 150

        # ---------------- ZEBRA CROSSING ----------------
        elif intervention_type == "ZEBRA_CROSSING":
            params["road_width_m"] = 7.0
            params["crossing_width_m"] = 3.0

        # ---------------- ROAD STUDS ----------------
        elif intervention_type == "ROAD_STUDS":
            params["length_m"] = length_m
            params["spacing_m"] = 10

        # ---------------- DELINEATORS ----------------
        elif intervention_type == "DELINEATOR":
            params["length_m"] = length_m
            params["spacing_m"] = 60

        # ---------------- POTHOLE ----------------
        elif intervention_type == "POTHOLE_REPAIR":
            params["area_m2"] = max(1.0, length_m * 0.5)
            params["depth_mm"] = 20

        # ---------------- STREET LIGHT ----------------
        elif intervention_type == "STREET_LIGHT":
            params["length_m"] = length_m

        # ---------------- SOLAR BLINKER ----------------
        elif intervention_type == "SOLAR_BLINKER":
            params["count"] = 1

        return params

    def extract_design_clause(self, intervention: str):
        """
    Extract ONLY clause explicitly written in intervention text.
    Handles:
      - clause 15.9 of IRC:67-2022
      - clause 5.4.6 and Table 5.1 of IRC:35-2015
    """

        clause_re = re.compile(
        r"clause\s*(\d+(?:\.\d+)*)"          # Clause number
        r"(?:\s*and\s*Table\s*\d+(?:\.\d+)*)?"  # Optional table
        r"\s*of\s*"
        r"IRC\s*[:\-]?\s*"                   # IRC prefix
        r"([A-Z]{1,4}(?:\s*:\s*\d+)?|\d+)"   # SP:73 OR 67 OR 35
        r"\s*[-–:\s]*"
        r"((19|20)\d{2})",                   # Year
        re.I
        )
        match = clause_re.search(intervention)
        if not match:
            return None

        clause_no = match.group(1)
        irc_code = match.group(2)
        year = match.group(3)

        return f"IRC:{irc_code}-{year} Clause {clause_no}"


    # ------------------------------------------------------------------
    # 4. MAIN ESTIMATION ENTRYPOINT
    # ------------------------------------------------------------------
    def estimate(self, intervention: str, clause_key: str, chainage_m: dict) -> Dict[str, Any]:

        intervention_type = self.classify_intervention(intervention)
        design_clause = self.extract_design_clause(intervention)

        if not intervention_type:
            return {
                "error": "Could not determine intervention type",
                "intervention": intervention,
                "clause_used": clause_key,
                "materials": {}
            }

        params = self.prepare_params(intervention_type, chainage_m)

        rule = self.qe.rulebook.get(intervention_type)
        if not rule:
            return {
                "error": f"No rulebook entry for {intervention_type}",
                "intervention": intervention,
                "clause_used": clause_key,
                "materials": {}
            }

        estimation = self.qe.estimate(intervention_type, params)

        return {
            "intervention": intervention,
            "clause_used": design_clause,
            "intervention_type": intervention_type,
            "params_used": estimation.get("params_used", params),
            "materials": estimation.get("materials", {})
            
        }
