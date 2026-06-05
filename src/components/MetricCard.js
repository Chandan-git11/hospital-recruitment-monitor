import React from "react";

function MetricCard({ title, value, detail }) {
  return (
    <div style={{
      background: "#ffffff",
      borderRadius: 12,
      boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
      padding: "20px",
      minWidth: 180,
      margin: "10px",
    }}>
      <div style={{ color: "#2d3748", fontSize: "14px", marginBottom: 10 }}>{title}</div>
      <div style={{ color: "#111827", fontSize: "32px", fontWeight: 700 }}>{value}</div>
      {detail && <div style={{ color: "#6b7280", marginTop: 8 }}>{detail}</div>}
    </div>
  );
}

export default MetricCard;
