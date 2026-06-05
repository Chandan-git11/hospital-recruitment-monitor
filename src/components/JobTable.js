import React from "react";

function JobTable({ jobs }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 20 }}>
      <thead>
        <tr>
          <th style={styles.th}>Title</th>
          <th style={styles.th}>Hospital</th>
          <th style={styles.th}>Location</th>
          <th style={styles.th}>Department</th>
          <th style={styles.th}>Job Type</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map((job, index) => (
          <tr key={index} style={styles.tr}>
            <td style={styles.td}>
              <a href={job.url} target="_blank" rel="noreferrer" style={{ color: "#2563eb" }}>
                {job.title}
              </a>
            </td>
            <td style={styles.td}>{job.hospital}</td>
            <td style={styles.td}>{job.location}</td>
            <td style={styles.td}>{job.department}</td>
            <td style={styles.td}>{job.job_type}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const styles = {
  th: {
    textAlign: "left",
    padding: "10px",
    borderBottom: "1px solid #e5e7eb",
    color: "#374151",
  },
  td: {
    padding: "10px",
    borderBottom: "1px solid #f3f4f6",
    color: "#1f2937",
  },
  tr: {
    backgroundColor: "#ffffff",
  },
};

export default JobTable;
