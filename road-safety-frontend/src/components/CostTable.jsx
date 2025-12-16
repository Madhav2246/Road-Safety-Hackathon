export default function CostTable({ boq }) {
  if (!boq) return <p>No BOQ data available</p>;

  return (
    <table className="boq-table">
      <thead>
        <tr>
          <th>Material</th>
          <th>Quantity</th>
          <th>Rate</th>
          <th>Total</th>
        </tr>
      </thead>

      <tbody>
        {Object.entries(boq.items || {}).map(([mat, row]) => (
          <tr key={mat}>
            <td>{mat}</td>
            <td>{row.quantity}</td>
            <td>{row.rate}</td>
            <td>{row.total}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
