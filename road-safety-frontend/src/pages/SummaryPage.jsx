import { useLocation, useNavigate } from "react-router-dom";
import "./SummaryPage.css";

export default function SummaryPage() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const result = state?.result;

  // =========================
  // SAFETY CHECK
  // =========================
  if (!result || !Array.isArray(result.interventions)) {
    return (
      <div className="summary-page page-error">
        <h2>No summary data available</h2>
        <button onClick={() => navigate("/")}>Go Home</button>
      </div>
    );
  }

  // =========================
  // DERIVED METRICS
  // =========================
  const totalInterventions = result.interventions.length;
  const grandTotal = result.grand_total ?? 0;
  const avgCost =
    totalInterventions > 0 ? grandTotal / totalInterventions : 0;

  // =========================
  // ACTIONS
  // =========================
  const exportPDF = () => window.print();
  const goBack = () => navigate(-1);
  const goToAnalytics = () =>
    navigate("/analytics", {
      state: { demographics: result.demographics },
    });

  // =========================
  // UI
  // =========================
  return (
    <div className="summary-page">
      {/* ================= ACTION BAR ================= */}
      <div className="summary-actions no-print">
        <button className="secondary-btn" onClick={goBack}>
          ← Back
        </button>

        <div className="action-group">
          <button className="secondary-btn" onClick={exportPDF}>
            Export PDF
          </button>
          <button className="primary-btn" onClick={goToAnalytics}>
            View Analytics
          </button>
        </div>
      </div>

      {/* ================= HERO ================= */}
      <section className="summary-hero">
        <h1>Cost Summary Report</h1>
        <p>
          Clause-backed, material-wise cost estimation derived from
          IRC standards and CPWD Schedule of Rates.
        </p>

        <div className="kpi-grid">
          <div className="kpi-card">
            <span>Total Interventions</span>
            <strong>{totalInterventions}</strong>
          </div>

          <div className="kpi-card">
            <span>Total Cost</span>
            <strong>
              ₹ {grandTotal.toLocaleString("en-IN")}
            </strong>
          </div>

          <div className="kpi-card">
            <span>Average Cost</span>
            <strong>
              ₹{" "}
              {avgCost.toLocaleString("en-IN", {
                maximumFractionDigits: 2,
              })}
            </strong>
          </div>
        </div>
      </section>

      {/* ================= INTERVENTIONS ================= */}
      <section className="interventions-section">
        <h2>Intervention-wise Breakdown</h2>

        <div className="intervention-grid">
          {result.interventions.map((item, index) => {
            const interventionCost = item?.cost?.total_cost ?? 0;
            const percentage =
              grandTotal > 0
                ? (interventionCost / grandTotal) * 100
                : 0;

            return (
              <div key={index} className="intervention-card">
                {/* HEADER */}
                <div className="intervention-header">
                  <h3>Intervention {index + 1}</h3>
                  <span className="cost-badge">
                    ₹ {interventionCost.toLocaleString("en-IN")}
                  </span>
                </div>

                {/* TEXT */}
                <p className="intervention-text">
                  {item.intervention}
                </p>

                {/* META */}
                <div className="meta">
                  <span>
                    Clause: {item.clause_used || "—"}
                  </span>
                  <span>
                    Chainage: {item.chainage || "—"}
                  </span>
                </div>

                {/* COST BAR */}
                <div className="cost-bar">
                  <div
                    className="cost-fill"
                    style={{ width: `${percentage}%` }}
                  />
                </div>

                {/* MATERIAL TABLE */}
                <table className="material-table">
                  <thead>
                    <tr>
                      <th>Material</th>
                      <th>Qty</th>
                      <th>Rate</th>
                      <th>Amount (₹)</th>
                    </tr>
                  </thead>

                  <tbody>
                    {(item.cost?.items || []).map((mat, i) => (
                      <tr key={i}>
                        <td>{mat.material}</td>
                        <td>{mat.qty}</td>
                        <td>{mat.rate ?? "-"}</td>
                        <td>
                          {mat.amount?.toLocaleString("en-IN", {
                            maximumFractionDigits: 2,
                          })}
                        </td>
                      </tr>
                    ))}

                    <tr className="subtotal-row">
                      <td colSpan="3">Subtotal</td>
                      <td>
                        ₹{" "}
                        {interventionCost.toLocaleString("en-IN")}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            );
          })}
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer className="summary-footer">
        Generated using IRC clauses, CPWD SOR datasets, and
        intelligent material quantification logic.
      </footer>
    </div>
  );
}
