import sqlite3
import difflib

DB_PATH = "database/sor.db"


def search_sor(material_query: str, year: int = None, limit=5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    q = material_query.lower()

    if year:
        cur.execute("SELECT item_code, description, unit, rate FROM sor_items WHERE year = ?", (year,))
    else:
        cur.execute("SELECT item_code, description, unit, rate FROM sor_items")

    rows = cur.fetchall()
    conn.close()

    # Best match via fuzzy search
    scored = []
    for item_code, desc, unit, rate in rows:
        score = difflib.SequenceMatcher(None, q, desc.lower()).ratio()
        scored.append((score, item_code, desc, unit, rate))

    scored.sort(reverse=True, key=lambda x: x[0])

    return scored[:limit]
