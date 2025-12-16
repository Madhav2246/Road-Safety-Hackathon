import os
from PyPDF2 import PdfReader

RAW_DIR = "data/irc_pdfs/raw"
OUT_DIR = "data/irc_pdfs/text_extracted"
os.makedirs(OUT_DIR, exist_ok=True)

for file in os.listdir(RAW_DIR):
    if not file.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(RAW_DIR, file)
    out_path = os.path.join(OUT_DIR, file.replace(".pdf", ".txt"))

    print(f"Extracting text from: {file}")

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        try:
            text += page.extract_text() + "\n"
        except:
            continue

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

print("\n✔ Text extraction completed. Check data/irc_pdfs/text_extracted/")
