// src/components/KPICard.jsx
import { useEffect, useRef, useState } from "react";
import "./KPICard.css";

export default function KPICard({ title, value, theme = "blue" }) {
  const [displayValue, setDisplayValue] = useState(0);
  const ref = useRef(null);

  useEffect(() => {
    let start = 0;
    const end = Number(value);
    if (isNaN(end)) return;

    const duration = 1200; // ms
    const increment = end / (duration / 16);

    let raf;

    const animate = () => {
      start += increment;
      if (start < end) {
        setDisplayValue(Math.floor(start));
        raf = requestAnimationFrame(animate);
      } else {
        setDisplayValue(end);
      }
    };

    animate();
    return () => cancelAnimationFrame(raf);
  }, [value]);

  return (
    <div ref={ref} className={`kpi-card ${theme}`}>
      <div className="kpi-title">{title}</div>
      <div className="kpi-value">{displayValue.toLocaleString()}</div>
      <div className="kpi-underline" />
    </div>
  );
}
