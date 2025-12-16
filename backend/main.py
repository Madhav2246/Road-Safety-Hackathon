# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.extract import router as extract_router
from api.routes.estimate import router as estimate_router
from api.routes.clauses import router as clause_router
from api.routes.cost import router as cost_router
from api.chatbot import router as chatbot_router
from api.process_all import router as process_router


app = FastAPI(title="Road Safety Estimation Backend")

# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

# 🔥 process-all already has /api prefix inside the file
app.include_router(process_router)
app.include_router(chatbot_router)
app.include_router(extract_router, prefix="/extract", tags=["Extract"])
app.include_router(clause_router, prefix="/clauses", tags=["Clauses"])
app.include_router(estimate_router, prefix="/estimate", tags=["Estimate"])
app.include_router(cost_router, prefix="/cost", tags=["Cost"])


@app.get("/")
def root():
    return {"message": "Backend running"}




