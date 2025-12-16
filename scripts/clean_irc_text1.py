"""
extract_irc_clauses.py

Run in the environment where your uploaded files are present (e.g. /mnt/data).
Produces: extracted_clauses.json
"""

import re
import os
import json
from glob import glob
from tqdm import tqdm

from sentence_transformers import SentenceTransformer, util
import numpy as np

# -------- CONFIG --------
DATA_DIR = "F:\\Hackathons\\Road Safety Hackathon (2)\\road-safety-estimator\\data\\irc_pdfs\\text_extracted"
OUT_JSON = os.path.join(DATA_DIR, "F:\\Hackathons\\Road Safety Hackathon (2)\\road-safety-estimator\\data\\irc_pdfs\\cleaned\\extracted_clauses.json")
REFERENCE_JSON = os.path.join(DATA_DIR, "F:\\Hackathons\\Road Safety Hackathon (2)\\Road Safety Hackathon\\data\\irc_clauses.json")  # your reference file
MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast; swap if you prefer larger
SIMILARITY_THRESHOLD = 0.68  # semantic match threshold to inherit metadata
# Candidate keywords to detect material items (expand as needed)
MATERIAL_KEYWORDS = [
    "sign", "thermoplastic", "paint", "road stud", "stud", "bituminous", "pothole",
    "solar blinker", "streetlight", "street light", "delineator", "fmm", "marker",
    "barrier", "guardrail", "lamp", "lamp post", "reflective", "tape", "glass bead",
    "thermoplastic paint", "bituminous mix", "road stud", "nos", "sqm"
]
# Default fallback metadata
FALLBACK = {"material_item_keyword": "misc", "default_quantity": 1, "default_unit": "nos"}

# -------- UTILITIES --------
def list_input_texts(data_dir=DATA_DIR):
    # look for the uploaded IRC text files (txt)
    patterns = ["*.txt"]
    files = []
    for p in patterns:
        files.extend(glob(os.path.join(data_dir, p)))
    # ignore the output file if it already exists
    files = [f for f in files if not f.endswith("extracted_clauses.json")]
    return sorted(files)

def read_text_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def clean_text(s):
    # basic cleaning for OCR noise: collapse multiple spaces, fix broken words at line ends
    s = s.replace("\r\n", "\n")
    s = re.sub(r"-\n\s*", "", s)  # join hyphenated line breaks
    s = re.sub(r"\n+", "\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    # collapse spaces around punctuation
    s = re.sub(r" \,", ",", s)
    return s.strip()

# Heuristic: find clause/section headings like '3.1', '14.8.8', 'Clause 3.1', 'clause 14.8.8'
CLAUSE_HEADING_RE = re.compile(
    r"(?P<head>(?:Clause|clause|Section|section)?\s*[:]?\s*(\d{1,2}(?:\.\d{1,3}){0,3}))\s*[:\-]?\s*",
    flags=re.IGNORECASE
)

def split_into_clauses(text):
    """
    Splits the document into chunks anchored by clause-like headings.
    Returns list of dicts: {doc_id, clause_id (may be None), text}
    """
    lines = text.splitlines()
    joined = "\n".join(lines)
    # find all clause headings
    matches = list(CLAUSE_HEADING_RE.finditer(joined))
    spans = []
    if not matches:
        # fallback: split into paragraphs
        paragraphs = [p.strip() for p in joined.split("\n\n") if p.strip()]
        return [{"clause_id": None, "text": clean_text(p)} for p in paragraphs]

    for i, m in enumerate(matches):
        start = m.start()
        clause_id = m.group(2)
        # start of content = end of heading
        content_start = m.end()
        if i+1 < len(matches):
            end = matches[i+1].start()
        else:
            end = len(joined)
        clause_text = joined[content_start:end].strip()
        # include heading in extracted text to preserve context
        full_text = f"{m.group(0).strip()} {clause_text}"
        spans.append({"clause_id": clause_id, "text": clean_text(full_text)})
    return spans

def keyword_material_item(text):
    """
    Rule-based keyword detection for material item keyword.
    Returns a single keyword (first match) or fallback.
    """
    t = text.lower()
    for kw in MATERIAL_KEYWORDS:
        if kw in t:
            return kw
    # basic noun extraction fallback: take first noun-like token (very simple)
    words = re.findall(r"[a-zA-Z\-]{3,}", t)
    return words[0] if words else FALLBACK["material_item_keyword"]

# -------- MAIN PROCESS --------
def main():
    # load model
    model = SentenceTransformer(MODEL_NAME)

    # load reference clauses (if present)
    reference_data = {}
    if os.path.exists(REFERENCE_JSON):
        with open(REFERENCE_JSON, "r", encoding="utf-8") as rf:
            try:
                reference_data = json.load(rf)
            except Exception as e:
                print("Warning: couldn't parse reference JSON:", e)

    # pre-embed reference texts for semantic matching
    ref_keys = list(reference_data.keys())
    ref_texts = [reference_data[k].get("text","") for k in ref_keys]
    if ref_texts:
        ref_embeddings = model.encode(ref_texts, convert_to_tensor=True, show_progress_bar=False)
    else:
        ref_embeddings = None

    # gather documents
    txt_files = list_input_texts(DATA_DIR)
    print(f"Found {len(txt_files)} .txt files to process.")
    docs = []
    for p in txt_files:
        text = read_text_file(p)
        doc_id = os.path.basename(p).replace(".txt", "")
        docs.append((doc_id, clean_text(text)))

    # extract clauses
    extracted = []  # list of dicts with doc_id, clause_id, text
    for doc_id, text in docs:
        spans = split_into_clauses(text)
        for s in spans:
            extracted.append({"doc_id": doc_id, "clause_id": s["clause_id"], "text": s["text"]})

    print(f"Extracted {len(extracted)} candidate clauses/chunks.")

    # embed extracted clauses in batches
    texts = [e["text"] for e in extracted]
    embeddings = model.encode(texts, convert_to_tensor=True, show_progress_bar=True)

    result_json = {}
    # For each extracted clause, try to match semantically to reference_data
    for idx, e in enumerate(tqdm(extracted, desc="matching clauses")):
        emb = embeddings[idx]
        best_match = None
        inherited = None
        if ref_embeddings is not None and len(ref_keys) > 0:
            # compute cosine similarities
            cos_scores = util.cos_sim(emb, ref_embeddings)[0]  # tensor of scores
            top_idx = int(np.argmax(cos_scores.cpu().numpy()))
            top_score = float(cos_scores[top_idx])
            if top_score >= SIMILARITY_THRESHOLD:
                best_key = ref_keys[top_idx]
                inherited = reference_data[best_key]
                best_match = (best_key, top_score)

        # Build key: prefer doc clause id if available, else derive safe key
        if e["clause_id"]:
            key = f"{e['doc_id']}_{e['clause_id']}"
        else:
            # create unique short id by taking first 6 chars of hash
            import hashlib
            h = hashlib.sha1(e["text"].encode("utf-8")).hexdigest()[:8]
            key = f"{e['doc_id']}_AUTO_{h}"

        # Construct entry text (shorten to one-line summary)
        text = e["text"]
        # try to make a concise text: first sentence or 200 chars
        first_sentence = re.split(r'(?<=[\.\?\!])\s+', text.strip())
        short_text = first_sentence[0].strip() if first_sentence and len(first_sentence[0])>20 else (text.strip()[:200] + ("..." if len(text)>200 else ""))

        entry = {"text": short_text}

        # inherit metadata if matched
        if inherited:
            entry["material_item_keyword"] = inherited.get("material_item_keyword", FALLBACK["material_item_keyword"])
            entry["default_quantity"] = inherited.get("default_quantity", FALLBACK["default_quantity"])
            entry["default_unit"] = inherited.get("default_unit", FALLBACK["default_unit"])
            entry["_matched_reference"] = best_match[0]
            entry["_similarity"] = round(best_match[1], 3)
        else:
            # rule-based extraction
            kw = keyword_material_item(text)
            entry["material_item_keyword"] = kw
            # small heuristic for units
            if kw in ("sqm", "square metre", "thermoplastic", "thermoplastic paint"):
                entry["default_unit"] = "sqm"
            elif kw in ("cum", "bituminous"):
                entry["default_unit"] = "cum"
            else:
                entry["default_unit"] = "nos"
            entry["default_quantity"] = 1

        # store extra metadata for debugging
        entry["_source_doc"] = e["doc_id"]
        entry["_clause_raw"] = text[:300]  # keep first 300 chars as preview
        result_json[key] = entry

    # Save JSON
    with open(OUT_JSON, "w", encoding="utf-8") as out_f:
        json.dump(result_json, out_f, indent=2, ensure_ascii=False)

    print("Done. Output written to:", OUT_JSON)
    print("Sample keys:", list(result_json.keys())[:10])

if __name__ == "__main__":
    main()
