import "../styles/intervention-card.css";

export default function InterventionCard({ index, data, updateField }) {
  return (
    <div className="intervention-row">
      {/* TIMELINE */}
      <div className="timeline">
        <div className="dot completed" />
        <div className="line" />
      </div>

      {/* CONTENT */}
      <div className="intervention-content">
        <div className="header">
          <span className="step">Intervention {index + 1}</span>
          <span className="status">Extracted</span>
        </div>

        <label>
          Intervention Description
          <textarea
            value={data.intervention}
            onChange={(e) =>
              updateField("intervention", e.target.value)
            }
            rows={3}
          />
        </label>

        <label>
          Chainage
          <input
            type="text"
            value={data.chainage}
            onChange={(e) =>
              updateField("chainage", e.target.value)
            }
            placeholder="e.g. 4+200 to 4+350"
          />
        </label>

        <div className="checklist">
          <span className="check done">PDF Parsed</span>
          <span className="check pending">Clause Matching</span>
          <span className="check pending">Cost Estimation</span>
        </div>
      </div>
    </div>
  );
}
