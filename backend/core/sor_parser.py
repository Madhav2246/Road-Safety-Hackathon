import pdfplumber, re, csv, os, pandas as pd
from tqdm import tqdm

def looks_hindi(text):
    """Detect Hindi pages by Unicode Devanagari range."""
    if not text:
        return False
    return any("\u0900" <= ch <= "\u097F" for ch in text)

def is_useless_page(text):
    """Skip forewords, prefaces, copyright, index pages."""
    if not text:
        return True
    
    bad_words = [
        "भारत सरकार", "सूचकांक", "सूचना", "हिन्दी", "foreword",
        "भारतीय मानक", "copyright", "index", "contents",
        "पुस्तक", "publication", "मूल्य", "संपादित"
    ]
    text_lower = text.lower()
    return any(word.lower() in text_lower for word in bad_words)

def clean_number(x):
    try:
        return float(str(x).replace(",", "").strip())
    except:
        return None

def normalize_desc(desc):
    """Clean unwanted spaces and line breaks."""
    if not desc:
        return ""
    desc = re.sub(r"\s+", " ", desc)
    return desc.strip()

def parse_sor_pdf(pdf_path, out_csv_path, year=None):
    rows = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)

        print(f"\n📘 Parsing SOR PDF: {pdf_path}")
        print(f"📄 Total Pages: {total_pages}\n")

        # Progress bar
        for i in tqdm(range(total_pages), desc="Extracting pages"):
            page = pdf.pages[i]
            page_num = i + 1
            
            text = page.extract_text() or ""

            # -------- PAGE FILTERING --------
            if looks_hindi(text):
                # print(f"Skipping Hindi page {page_num}")
                continue

            if is_useless_page(text):
                # print(f"Skipping useless page {page_num}")
                continue

            # -------- TRY EXTRACT TABLE --------
            table = page.extract_table()

            if table:
                headers = [h.strip().lower() if h else "" for h in table[0]]
                
                # Extract each row
                for rid, row in enumerate(table[1:]):
                    row_dict = dict(zip(headers, row))

                    item_code = row_dict.get("item") or row_dict.get("code") or ""
                    desc = row_dict.get("description") or row_dict.get("item description") or ""
                    unit = row_dict.get("unit") or row_dict.get("uom") or ""
                    rate = row_dict.get("rate") or row_dict.get("value") or ""

                    rows.append({
                        "year": year,
                        "page": page_num,
                        "row_index": rid,
                        "item_code": item_code.strip(),
                        "description": normalize_desc(desc),
                        "unit": unit.strip(),
                        "unit_rate": clean_number(rate),
                    })
            else:
                # -------- REGEX FALLBACK --------
                for ln in text.splitlines():
                    m = re.match(
                        r"^([0-9.]+)\s+(.+?)\s+([A-Za-z/]+)\s+([\d,]+\.\d+)$", ln
                    )
                    if m:
                        item_code, desc, unit, rate = m.groups()
                        rows.append({
                            "year": year,
                            "page": page_num,
                            "row_index": None,
                            "item_code": item_code.strip(),
                            "description": normalize_desc(desc),
                            "unit": unit.strip(),
                            "unit_rate": clean_number(rate),
                        })

    # Convert to CSV
    df = pd.DataFrame(rows)
    df.to_csv(out_csv_path, index=False)

    print(f"\n✅ Extraction complete: {len(rows)} rows saved to {out_csv_path}")
    return len(rows)
