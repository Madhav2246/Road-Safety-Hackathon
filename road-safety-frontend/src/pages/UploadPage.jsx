// src/pages/UploadPage.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/backend";
import "./UploadPage.css";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const el = document.querySelector(".upload-card");
    setTimeout(() => el.classList.add("active"), 100);
  }, []);

  const handleProcess = async () => {
    if (!file) {
      alert("Please upload a PDF report");
      return;
    }

    const form = new FormData();
    form.append("file", file);

    setLoading(true);
    try {
      const data = await api.uploadPDF(form);
      navigate("/results", { state: { extracted: data } });
    } catch (err) {
      alert("Backend error. Check console.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="upload-root">
      {/* HEADER */}
      <header className="gov-header">
        <div className="gov-brand">
          <span className="gov-title">
            Road Safety Cost Estimation System
          </span>
          <span className="gov-subtitle">
            Decision Support Platform
          </span>
        </div>

        <nav className="gov-nav">
          <button onClick={() => navigate("/")}>Home</button>
        </nav>
      </header>

      {/* CONTENT */}
      <main className="upload-container">
        <div className="upload-card reveal">
          <h1>Upload Road Safety Report</h1>
          <p className="desc">
            Upload an IRC-based road safety audit or intervention report
            to generate clause-backed material quantities and
            CPWD-aligned cost estimates.
          </p>

          <label className="upload-box">
            <input
              type="file"
              accept=".pdf"
              hidden
              onChange={(e) => setFile(e.target.files[0])}
            />

            <div className="upload-icon">PDF</div>

            <p className="upload-text">
              {file ? file.name : "Click to select PDF file"}
            </p>

            <span className="upload-hint">
              Accepted format: Road Safety Audit / Intervention Report
            </span>
          </label>

          <button
            className="primary-btn full"
            onClick={handleProcess}
            disabled={loading}
          >
            {loading ? "Processing Report..." : "Generate Cost Estimate"}
          </button>

          <div className="upload-footer">
            Powered by IRC Clauses • CPWD Schedule of Rates • AI Cost Engine
          </div>
        </div>
      </main>
    </div>
  );
}
