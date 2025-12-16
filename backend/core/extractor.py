# backend/core/extractor.py
import fitz
import re


# ============================================================
# PDF TEXT
# ============================================================

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = []
    for p in doc:
        t = p.get_text("text")
        if t:
            text.append(t)
    return "\n".join(text)


# ============================================================
# PARSE A CHAINAGE STRING LIKE "4+200"
# ============================================================

def chain_to_meters(c):
    m = re.match(r"(\d+)\s*\+\s*(\d+)", c)
    if not m:
        return None
    return int(m.group(1)) * 1000 + int(m.group(2))


# ============================================================
# EXTRACT INTERVENTIONS (FINAL, CORRECT, COLUMN-AWARE)
# ============================================================
def extract_interventions(text):
    # Remove headers / footers
    text = re.sub(r"Road Safety Intervention Report|CoERS|IIT|Hackathon|Page\s*\d+", " ", text, flags=re.I)

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    results = []

    i = 0
    n = len(lines)

    # Regex patterns from high-accuracy parser
    action_re = re.compile(
        r"\b(shall be|should be|to be|replace|replaced|install|installed|provide|provided|repaint|paint|shall\s+be\s+provided|shall\s+be\s+replaced)\b",
        re.I,
    )
    clause_start_re = re.compile(r"clause\s*\d+(\.\d+)*", re.I)
    observation_re = re.compile(
        r"\b(missing|non[-\s]?standard|damaged|faded|absent|broken|not provided|worn out|poor condition)\b",
        re.I,
    )
    clause_full_re = re.compile(
        r"clause\s*\d+(\.\d+)*\s*(and\s*Table\s*\d+(\.\d+)*)*\s*of\s*IRC\s*[:\-\s]*[A-Za-z0-9\.:]+[-\s:]*((19|20)\d{2})",
        re.I,
    )
    year_re = re.compile(r"\b(19|20)\d{2}\b")

    while i < n:
        ln = lines[i]

        # detect chainage row
        if re.match(r"^\d+\s*\+\s*\d+$", ln):

            # ------ CHAINAGE EXTRACTION (unchanged) ------
            start_chain = ln
            start_m = chain_to_meters(start_chain)

            end_chain = start_chain
            end_m = start_m

            if i + 1 < n and lines[i+1].lower() == "to":
                if i + 2 < n and re.match(r"^\d+\s*\+\s*\d+$", lines[i+2]):
                    end_chain = lines[i+2]
                    end_m = chain_to_meters(end_chain)
                    i += 3
                else:
                    i += 1

            elif i + 1 < n and lines[i+1] == "&":
                if i + 2 < n and re.match(r"^\d+\s*\+\s*\d+$", lines[i+2]):
                    end_chain = lines[i+2]
                    end_m = chain_to_meters(end_chain)
                    i += 3
                else:
                    i += 1

            else:
                i += 1

            # build chainage text
            if start_m == end_m:
                chainage_text = start_chain
            else:
                chainage_text = f"{start_chain} to {end_chain}"

            # ------ NEW: HIGH-ACCURACY OBS + INTERVENTION EXTRACTION ------
            obs_text = ""
            inter_text = ""
            buffer = ""
            collecting = False

            while i < n:
                # stop when next chainage comes
                if re.match(r"^\d+\s*\+\s*\d+$", lines[i]):
                    break

                ln2 = lines[i].strip()

                # Identify OBSERVATION
                if observation_re.search(ln2) and not action_re.search(ln2):
                    obs_text += " " + ln2
                    i += 1
                    continue

                # Identify START OF INTERVENTION
                if action_re.search(ln2):
                    collecting = True
                    buffer += " " + ln2
                    i += 1
                    continue

                # Continue adding intervention lines
                if collecting:
                    buffer += " " + ln2
                    i += 1
                    continue

                i += 1

            # Clean intervention text
            inter_text = re.sub(r"\s+", " ", buffer).strip()
            obs_text = re.sub(r"\s+", " ", obs_text).strip()

            if not inter_text:
                continue

            # Final validation (same as your good code)
            if not (action_re.search(inter_text) and (clause_start_re.search(inter_text) or year_re.search(inter_text))):
                continue

            # finalize record
            results.append({
                "observation": obs_text,
                "intervention": inter_text,
                "chainage": chainage_text,
                "chainage_m": {
                    "start_m": start_m,
                    "end_m": end_m,
                    "length_m": abs(end_m - start_m)
                }
            })

        else:
            i += 1

    return results

