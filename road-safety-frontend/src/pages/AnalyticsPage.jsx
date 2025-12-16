import { useLocation } from "react-router-dom";
import KPICard from "../components/KPICard";
import ClauseBarChart from "../components/ClauseBarChart";
import MaterialPieChart from "../components/MaterialPieChart";
import "./AnalyticsPage.css";

export default function AnalyticsPage() {
  const { state } = useLocation();
  const demo = state?.demographics;

  // -----------------------------
  // Safety check
  // -----------------------------
  if (!demo) {
    return (
      <div className="analytics-page">
        <p>No analytics data.</p>
      </div>
    );
  }

  // -----------------------------
  // UI
  // -----------------------------
  return (
    <div className="analytics-page">
      {/* ================= HEADER ================= */}
      <div className="analytics-header">
        <h1 className="analytics-title">
          Cost Analytics Dashboard
        </h1>
        <p className="analytics-subtitle">
          Clause-wise and material-wise cost intelligence
        </p>
      </div>

      {/* ================= KPI CARDS ================= */}
      <div className="kpi-grid">
        <KPICard
          title="Total Interventions"
          value={demo.kpis.total_interventions}
          theme="blue"
        />

        <KPICard
          title="IRC Clauses Used"
          value={demo.kpis.unique_clauses}
          theme="purple"
        />

        <KPICard
          title="Total Cost (₹)"
          value={demo.kpis.grand_total.toFixed(0)}
          theme="green"
        />
      </div>

      {/* ================= CHARTS ================= */}
      <div className="chart-grid">
        <div className="chart-card">
          <h2>Cost Distribution by IRC Clause</h2>
          <div className="chart-wrapper">
            <ClauseBarChart data={demo.by_clause} />
          </div>
        </div>

        <div className="chart-card">
          <h2>Material-wise Cost Share</h2>
          <div className="chart-wrapper">
            <MaterialPieChart data={demo.materials} />
          </div>
        </div>
      </div>
    </div>
  );
}
