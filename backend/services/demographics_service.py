# backend/services/demographics_service.py

from collections import defaultdict

class DemographicsService:

    @staticmethod
    def compute(interventions):
        by_clause = defaultdict(lambda: {"count": 0, "total_cost": 0.0})
        materials = defaultdict(float)

        for item in interventions:
            clause = item.get("clause_used") or "UNKNOWN"
            cost_block = item.get("cost", {})

            total_cost = cost_block.get("total_cost", 0.0)
            items = cost_block.get("items", [])   # ✅ FIX HERE

            # Clause aggregation
            by_clause[clause]["count"] += 1
            by_clause[clause]["total_cost"] += total_cost

            # Material aggregation
            for m in items:
                mat_name = m.get("material")
                amount = m.get("amount", 0.0)

                if mat_name:
                    materials[mat_name] += amount

        return {
            "by_clause": dict(by_clause),
            "materials": dict(materials),
            "kpis": {
                "total_interventions": len(interventions),
                "unique_clauses": len(by_clause),
                "grand_total": round(
                    sum(v["total_cost"] for v in by_clause.values()), 2
                ),
            },
        }
