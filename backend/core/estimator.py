from core.rag_retriever import retrieve_sor_items

def price_material(material_description, quantity, preferred_unit=None):
    # 1. Retrieve candidate SOR items
    candidates = retrieve_sor_items(material_description, top_k=6)
    # 2. Heuristic: prefer same unit
    if preferred_unit:
        same_unit = [c for c in candidates if c["unit"] and preferred_unit.lower() in c["unit"].lower()]
        if same_unit:
            chosen = same_unit[0]
        else:
            chosen = candidates[0] if candidates else None
    else:
        chosen = candidates[0] if candidates else None

    if not chosen or chosen["unit_rate"] is None:
        return {"quantity": quantity, "selected_item": None, "unit_rate": None, "amount": None, "candidates": candidates}

    # Convert units if necessary (you'll need a unit conversion table, e.g., kg<->m3 etc.)
    amount = float(quantity) * float(chosen["unit_rate"])
    return {
        "quantity": quantity,
        "selected_item": chosen,
        "unit_rate": chosen["unit_rate"],
        "amount": amount,
        "candidates": candidates
    }
