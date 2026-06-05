import React, { useEffect, useState } from "react";
import HomePage from "./pages/HomePage";

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/jobs")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load jobs");
        }
        return response.json();
      })
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ fontFamily: "Inter, system-ui, sans-serif", background: "#f3f4f6", minHeight: "100vh" }}>
      <header style={{ padding: 24, background: "#1f2937", color: "#ffffff" }}>
        <h1 style={{ margin: 0 }}>Hospital Career Pages Monitor</h1>
        <p style={{ marginTop: 8, color: "#9ca3af" }}>Monitoring hospital job board listings in real time.</p>
      </header>
      <main>
        {loading && <div style={{ padding: 24 }}>Loading jobs...</div>}
        {error && <div style={{ padding: 24, color: "#b91c1c" }}>{error}</div>}
        {!loading && !error && <HomePage jobs={jobs} />}
      </main>
    </div>
  );
}

export default App;
