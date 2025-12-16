export default function InterventionCard({ index, data, updateField }) {
  return (
    <div className="card">
      <h3>Intervention #{index + 1}</h3>

      
      <input
        className="input"
        value={data.intervention}
        onChange={(e) => updateField("intervention", e.target.value)}
        placeholder="Intervention text"
      />

      <input
        className="input"
        value={data.chainage}
        onChange={(e) => updateField("chainage_text", e.target.value)}
        placeholder="Chainage Text"
      />

      

      
    </div>
  );
}
