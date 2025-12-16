// src/pages/ResultsPage.jsx
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import InterventionRow from "../components/InterventionRow";
import { api } from "../api/backend";
import "./ResultsPage.css";

export default function ResultsPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const extracted = state?.extracted;

  const [interventions, setInterventions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!extracted || !Array.isArray(extracted.interventions)) {
      alert("No extracted data found. Please upload the PDF again.");
      navigate("/");
      return;
    }

    const normalized = extracted.interventions.map((item, idx) => ({
      id: idx + 1,
      intervention: item.intervention,
      chainage: item.chainage,
    }));

    setInterventions(normalized);
  }, [extracted, navigate]);

  const updateIntervention = (index, key, value) => {
    setInterventions((prev) => {
      const updated = [...prev];
      updated[index][key] = value;
      return updated;
    });
  };

  const runAll = async () => {
    try {
      setLoading(true);
      const result = await api.processAll(interventions);
      navigate("/summary", { state: { result } });
    } catch (err) {
      alert("Cost estimation failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="results-root">
      <header className="gov-header sticky">
        <div>
          <div className="gov-title">Road Safety Cost Estimation System</div>
          <div className="gov-subtitle">Intervention Review</div>
        </div>
        <button onClick={() => navigate("/upload")}>
          Upload New Report
        </button>
      </header>

      <main className="results-main">
        <section className="results-panel">
          <h1>Review Extracted Interventions</h1>
          <p>
            The following interventions were automatically extracted from
            the uploaded road safety report. Please review before
            generating cost estimates.
          </p>

          <div className="intervention-list">
            {interventions.map((item, i) => (
              <InterventionRow
                key={item.id}
                index={i}
                data={item}
                updateField={(key, value) =>
                  updateIntervention(i, key, value)
                }
              />
            ))}
          </div>

          <div className="action-bar">
            <button
              className="primary-btn"
              onClick={runAll}
              disabled={loading}
            >
              {loading
                ? "Computing Cost Estimates..."
                : "Generate Consolidated Cost Estimate"}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
