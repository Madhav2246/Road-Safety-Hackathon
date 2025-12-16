import os
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------------------------------------
# Load ENV
# --------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use quota-friendly model
MODEL_NAME = "models/gemini-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)

# --------------------------------------------------
# FALLBACK ENGINE (NO API)
# --------------------------------------------------
def fallback_answer(question: str, context: str) -> str:
    q = question.lower()

    if "cost" in q:
        return (
            "The cost is driven by IRC-mandated materials such as "
            "retro-reflective sheeting, MS posts, and concrete foundations. "
            "Higher safety zones (schools, junctions) require stricter compliance, "
            "leading to increased costs."
        )

    if "clause" in q or "irc" in q:
        return (
            "IRC clauses define standardized safety requirements. "
            "Each clause specifies materials, dimensions, and placement rules, "
            "which directly influence quantity and cost estimation."
        )

    if "chart" in q or "analytics" in q:
        return (
            "The chart highlights cost concentration areas. "
            "Clauses with higher bars or pie shares indicate interventions "
            "that consume a larger portion of the total budget."
        )

    return (
        "This system provides explanations only for road safety cost analysis, "
        "IRC clauses, and related analytics."
    )

# --------------------------------------------------
# MAIN CHAT FUNCTION
# --------------------------------------------------
def ask_gemini(question: str, context: str) -> str:
    prompt = f"""
You are a Road Safety Cost Estimation assistant.

RULES:
- Answer ONLY using the context
- Focus on IRC clauses, costs, analytics
- Be concise and professional

CONTEXT:
{context}

QUESTION:
{question}
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        # 🔥 QUOTA SAFE FALLBACK
        if "429" in str(e) or "quota" in str(e).lower():
            return fallback_answer(question, context)

        return "The analysis engine is temporarily unavailable. Please try again."
