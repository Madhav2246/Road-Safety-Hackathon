// src/pages/HomePage.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();

  useEffect(() => {
    const reveals = document.querySelectorAll(".reveal");

    const onScroll = () => {
      reveals.forEach((el) => {
        const top = el.getBoundingClientRect().top;
        const visible = window.innerHeight - 120;
        if (top < visible) el.classList.add("active");
      });
    };

    window.addEventListener("scroll", onScroll);
    onScroll();

    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className="home-root">
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
          <a href="#overview">Overview</a>
          <a href="#standards">Standards</a>
          <a href="#analytics">Analytics</a>
          <button onClick={() => navigate("/upload")}>
            Start Assessment
          </button>
        </nav>
      </header>

      {/* HERO */}
      <section className="hero">
        <h1>
          Intelligent Cost Estimation for Road Safety Interventions
        </h1>
        <p>
          A national-standards-aligned platform that converts road safety
          audit reports into clause-backed, itemised, and defensible
          cost estimates.
        </p>

        <button
          className="primary-btn"
          onClick={() => navigate("/upload")}
        >
          Upload Road Safety Report
        </button>
      </section>

      {/* OVERVIEW */}
      <section id="overview" className="section light reveal">
        <h2>Problem Statement</h2>
        <p>
          Road safety interventions are frequently planned using manual
          estimation practices, fragmented technical standards, and
          inconsistent cost references. These limitations lead to
          inaccurate budgeting, prolonged approval cycles, and
          difficulty in justifying safety investments.
        </p>
        <p>
          This platform addresses these challenges by introducing a
          unified, standards-driven cost estimation workflow that
          ensures transparency, repeatability, and auditability.
        </p>
      </section>

      {/* STANDARDS */}
      <section id="standards" className="section dark reveal">
        <h2>Standards & Data Sources</h2>

        <div className="workflow">
          <div className="step">
            <h3>IRC Standards</h3>
            <p>
              Automated clause identification and mapping using IRC:67,
              IRC:35, and related Indian Roads Congress codes governing
              road safety infrastructure.
            </p>
          </div>

          <div className="step">
            <h3>CPWD Schedule of Rates</h3>
            <p>
              Item-wise material costing aligned with official CPWD SOR
              datasets, ensuring compliance with government-approved
              rate structures.
            </p>
          </div>

          <div className="step">
            <h3>Chainage-Aware Quantification</h3>
            <p>
              Material quantities dynamically computed using chainage,
              intervention span, and geometric parameters extracted
              from audit reports.
            </p>
          </div>
        </div>
      </section>

      {/* ANALYTICS */}
      <section id="analytics" className="section light reveal">
        <h2>Decision-Oriented Analytics</h2>
        <p>
          The system generates intervention-wise, clause-wise, and
          material-wise cost summaries, enabling planners and engineers
          to identify high-impact safety measures and optimize limited
          budgets.
        </p>
        <p>
          Analytics outputs support evidence-based decision-making,
          funding justification, and prioritisation of safety
          interventions across road networks.
        </p>
      </section>

      {/* FOOTER */}
      <footer className="gov-footer">
        <div>Road Safety Cost Estimation System</div>
        <span>
          Academic & Research Prototype • Hackathon Submission
        </span>
        <span>
          Built using IRC standards and CPWD Schedule of Rates
        </span>
      </footer>
    </div>
  );
}
