from core.embeddings import query_index
from core.db import Session, SORItem

def retrieve_sor_items(material_text, top_k=5):
    candidates = query_index(material_text, top_k=top_k)
    # fetch DB rows for candidate ids
    session = Session()
    results = []
    for c in candidates:
        item = session.query(SORItem).filter(SORItem.id==c["id"]).first()
        if item:
            results.append({
                "sor_item_id": item.id,
                "item_code": item.item_code,
                "description": item.description,
                "unit": item.unit,
                "unit_rate": item.unit_rate,
                "score": c["score"]
            })
    session.close()
    # optionally post-rank using lexical match or heuristics (prefer same unit)
    results = sorted(results, key=lambda x: (x["unit_rate"] is not None, x["score"]), reverse=True)
    return results
