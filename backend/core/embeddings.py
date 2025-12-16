from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

MODEL = SentenceTransformer('all-MiniLM-L6-v2')
INDEX_PATH = "backend/data/faiss_index/sor_index.pkl"
META_PATH = "backend/data/faiss_index/sor_meta.pkl"

def build_index(descriptions, ids):
    # descriptions: list[str], ids: list[int] corresponding to SORItem.id
    embeddings = MODEL.encode(descriptions, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    # save index and metadata
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH.replace(".pkl","_faiss.index"))
    with open(META_PATH, "wb") as f:
        pickle.dump({"ids": ids, "descriptions": descriptions}, f)
    return True

def query_index(query, top_k=5):
    q_emb = MODEL.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    index = faiss.read_index(INDEX_PATH.replace(".pkl","_faiss.index"))
    D, I = index.search(q_emb, top_k)
    # load meta
    import pickle
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)
    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < 0: continue
        results.append({"id": meta["ids"][idx], "desc": meta["descriptions"][idx], "score": float(score)})
    return results
