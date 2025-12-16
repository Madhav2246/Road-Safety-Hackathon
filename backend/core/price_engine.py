# backend/core/price_engine.py
import os
import csv
import json
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle

DEFAULT_INDEX_DIR = "data/sor_index"
DEFAULT_CSV_DIR = "data/sor_csv"

class PriceIndex:
    def __init__(self, items: List[Dict[str,Any]], vectorizer=None, tfidf_matrix=None, index_dir=DEFAULT_INDEX_DIR):
        self.items = items
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.index_dir = index_dir
        self.row_count = len(items)

def read_csv_rows(path: str) -> List[Dict[str,str]]:
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            # normalize keys
            rows.append({k.strip(): (v.strip() if v else "") for k,v in r.items()})
    return rows

def build_index_from_csv(csv_paths: List[str], index_dir: str = DEFAULT_INDEX_DIR) -> PriceIndex:
    all_items = []
    texts = []
    for p in csv_paths:
        if not os.path.exists(p):
            continue
        rows = read_csv_rows(p)
        for r in rows:
            desc = r.get("description") or r.get("desc") or r.get("item_description") or ""
            unit = r.get("unit") or r.get("uom") or ""
            rate = r.get("rate") or r.get("price") or r.get("rate_per_unit") or ""
            item = {"description": desc, "unit": unit, "rate": rate, "source": p}
            all_items.append(item)
            texts.append(desc)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=20000)
    if texts:
        tfidf = vectorizer.fit_transform(texts)
    else:
        tfidf = None
    idx = PriceIndex(all_items, vectorizer=vectorizer, tfidf_matrix=tfidf, index_dir=index_dir)
    os.makedirs(index_dir, exist_ok=True)
    with open(os.path.join(index_dir, "items.pkl"), "wb") as f:
        pickle.dump(all_items, f)
    with open(os.path.join(index_dir, "vec.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    if tfidf is not None:
        with open(os.path.join(index_dir, "tfidf.npz"), "wb") as f:
            pickle.dump(tfidf, f)
    return idx

def load_index(index_dir: str = DEFAULT_INDEX_DIR) -> PriceIndex:
    import pickle
    items_path = os.path.join(index_dir, "items.pkl")
    vec_path = os.path.join(index_dir, "vec.pkl")
    tfidf_path = os.path.join(index_dir, "tfidf.npz")
    if not os.path.exists(items_path):
        return PriceIndex([], None, None, index_dir=index_dir)
    with open(items_path, "rb") as f:
        items = pickle.load(f)
    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)
    try:
        with open(tfidf_path, "rb") as f:
            tfidf = pickle.load(f)
    except Exception:
        tfidf = None
    idx = PriceIndex(items, vectorizer=vectorizer, tfidf_matrix=tfidf, index_dir=index_dir)
    return idx

def lookup_price(idx: PriceIndex, query: str, top_k: int = 5) -> List[Dict[str,Any]]:
    if not idx or not idx.vectorizer or idx.tfidf_matrix is None or not idx.items:
        return []
    qvec = idx.vectorizer.transform([query])
    sims = linear_kernel(qvec, idx.tfidf_matrix).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    results = []
    for i in top_idx:
        r = idx.items[i].copy()
        r["score"] = float(sims[i])
        results.append(r)
    return results
