import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Cell,
} from "recharts";

const COLORS = [
  "#2563eb",
  "#16a34a",
  "#f59e0b",
  "#dc2626",
  "#9333ea",
  "#14b8a6",
];

export default function MaterialPieChart({ data }) {
  const chartData = Object.entries(data).map(([k, v]) => ({
    name: k.replace("_", " "),
    value: Number(v.toFixed(2)),
  }));

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            innerRadius={50}
            outerRadius={100}
            paddingAngle={3}
          >
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
