# backend/api/routes/extract.py
from fastapi import APIRouter, UploadFile, File
import os
from core.extractor import read_pdf, extract_interventions

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/pdf")
async def extract_from_pdf(file: UploadFile = File(...)):
    print("\n--- Incoming PDF Upload ---")
    print("Filename:", file.filename)
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print("Saved to:", file_path)

        # Read text
        try:
            text = read_pdf(file_path)
            print("TEXT LENGTH:", len(text))
        except Exception as e:
            print("PDF READ ERROR:", e)
            return {"error": f"PDF reading failed: {str(e)}", "step": "read_pdf"}

        if not text or not text.strip():
            return {"error": "PDF text extraction returned empty text", "step": "read_pdf_empty"}

        # Extract interventions
        try:
            interventions = extract_interventions(text)
            print("INTERVENTION COUNT:", len(interventions))
        except Exception as e:
            print("INTERVENTION EXTRACT ERROR:", e)
            return {"error": f"Intervention extraction failed: {str(e)}", "step": "extract_interventions"}

        if not interventions:
            return {"warning": "No interventions detected", "filename": file.filename, "count": 0, "interventions": []}

        return {"filename": file.filename, "count": len(interventions), "interventions": interventions}

    except Exception as e:
        print("SERVER ERROR:", e)
        return {"error": f"Unexpected server error: {str(e)}", "step": "unknown"}
