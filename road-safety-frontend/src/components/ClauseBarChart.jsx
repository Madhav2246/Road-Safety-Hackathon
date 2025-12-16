import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

export default function ClauseBarChart({ data }) {
  const chartData = Object.entries(data).map(([k, v]) => ({
    clause: k.replace("_", " "),
    cost: Number(v.total_cost.toFixed(2)),
  }));

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <XAxis dataKey="clause" hide />
          <YAxis />
          <Tooltip />
          <Bar dataKey="cost" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
