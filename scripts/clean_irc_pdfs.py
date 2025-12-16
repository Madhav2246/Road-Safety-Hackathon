# scripts/clean_irc_pdfs.py
import os
import argparse
from pathlib import Path
from tqdm import tqdm
import subprocess

"""
Cleans PDFs:
 - runs ocrmypdf on each file in data/irc_pdfs/raw
 - outputs to data/irc_pdfs/cleaned with same filename
"""

# ---------- FIXED ABSOLUTE PATH HANDLING ----------
# Automatically detect project root and build exact path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
IRC_BASE_DIR = PROJECT_ROOT / "data" / "irc_pdfs"


def ensure_dirs():
    raw = IRC_BASE_DIR / "raw"
    cleaned = IRC_BASE_DIR / "cleaned"

    raw.mkdir(parents=True, exist_ok=True)
    cleaned.mkdir(parents=True, exist_ok=True)

    return raw, cleaned


def run_ocrmypdf(input_path: Path, out_path: Path, force=False):
    args = [
        "ocrmypdf",
        "--deskew",
        "--rotate-pages",
        "--optimize", "1",
        "--remove-background",
        str(input_path),
        str(out_path)
    ]
    
    if force:
        args.insert(1, "--force-ocr")

    try:
        subprocess.run(args, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ocrmypdf failed for {input_path}: {e}")
        return False


def main(force=False):
    raw, cleaned = ensure_dirs()

    print("\nLooking for PDFs in:", raw, "\n")

    files = sorted(raw.glob("*.pdf"))
    if not files:
        print("No PDFs found in", raw)
        return

    for f in tqdm(files, desc="OCR'ing PDFs"):
        out = cleaned / f.name
        if out.exists() and not force:
            print(f"Skipping (exists): {out}")
            continue

        ok = run_ocrmypdf(f, out, force=force)
        if not ok:
            print("Failed OCR:", f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force OCR even if output exists")
    args = parser.parse_args()

    main(force=args.force)
