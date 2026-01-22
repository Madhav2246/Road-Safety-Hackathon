
# 🚦 AI-Powered Road Safety Intelligence System

## 📌 Overview
This project is a full-stack **AI-powered Road Safety Intelligence Platform** that automates the end-to-end analysis of road safety audit reports. The system extracts safety interventions from unstructured PDF documents, maps them to relevant **IRC standards**, estimates material-only costs using **SOR / CPWD / GeM datasets**, and provides rich analytics and conversational insights via an integrated AI chatbot.

Designed as a **modular, scalable decision-support system**, this platform significantly reduces manual effort in road safety auditing and enables faster, standards-compliant engineering decisions.

---

## 🧩 System Architecture

### 🔹 Frontend (React)
- Built with **React + React Router**
- Modular, component-based UI
- Clear workflow-driven pages:
  - Home → Upload → Results → Summary → Analytics
- Floating **context-aware ChatBot** available across result pages

### 🔹 Backend (Python)
- REST-based API architecture
- Modular pipelines for:
  - NLP extraction
  - IRC clause matching
  - Cost estimation
  - Analytics & chatbot reasoning

## 🔍 Core Features

### 📄 Document Ingestion
- Upload road safety audit PDF/Text reports
- Robust extraction using PyMuPDF / pdfplumber
- Automatic chainage parsing (e.g., `4+200 to 4+500` → meters)

### 🧠 NLP-Based Intervention Extraction
- Hybrid NLP pipeline (rule-based + ML)
- Dependency parsing and phrase extraction
- Converts unstructured text into structured interventions

### 📚 IRC Clause Matching
- Semantic similarity using **TF-IDF + cosine similarity**
- Rulebook-driven validation
- Supports IRC:73, IRC:35, IRC:SP guidelines

### 💰 Intelligent Cost Estimation
- Builds price index from SOR / CPWD / GeM CSVs
- TF-IDF based description-to-item matching
- Editable quantities and cost overrides
- Material-only cost computation

### 📊 Analytics & Decision Insights
- KPI cards (total interventions, total cost)
- Clause-wise bar charts
- Material-wise cost pie charts
- Summary dashboards for engineers and planners

### 🤖 Context-Aware AI Chatbot
- Integrated across result pages
- Uses extracted interventions and analytics as context
- Supports follow-up reasoning and explanations
- Built using RAG-style retrieval + LLM integration

---

## 🛠️ Technologies Used

### Frontend
- React
- React Router
- Axios
- Plotly / Custom Charts

### Backend
- Python
- FastAPI-style routing
- spaCy
- Scikit-learn (TF-IDF, cosine similarity)

### Data & Intelligence
- CPWD / SOR datasets
- IRC standards (JSON-based rulebooks)
- Semantic search & rule-based reasoning

---

## 📈 Results & Impact
- Automated extraction of road safety interventions
- Accurate mapping to IRC clauses
- Rapid, editable cost estimation
- Significant reduction in manual audit interpretation time
- Scalable architecture suitable for state and national deployment

---

## 🔮 Future Enhancements
- GIS-based accident heatmaps
- ML-based accident risk prediction
- Real-time IoT traffic data ingestion
- Fine-tuned LLM for IRC semantic reasoning
- Government dashboard integration

---

## 👨‍💻 Author
**Madhav Yalamarthi**  
**Katakam Madhuri**
AI | NLP | Full-Stack Applied AI Systems

---

## 📜 License
This project is intended for academic, research, and hackathon use.
