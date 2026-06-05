import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import MetricCard from "../components/MetricCard";
import JobTable from "../components/JobTable";

function HomePage({ jobs }) {

const [locationData, setLocationData] = useState([]);
const [departmentData, setDepartmentData] = useState([]);
  useEffect(() => {

    fetch("http://127.0.0.1:5000/api/analytics/locations")
      .then((res) => res.json())
      .then((data) => {

        const formatted =
          Object.entries(data).map(
            ([location, value]) => ({
              location,
              value
            })
          );

        setLocationData(formatted);
      })
      .catch((err) => {
        console.error(
          "Location analytics error:",
          err
        );
      });

  }, []);

  const totalJobs = jobs.length;

  const jobsByHospital = jobs.reduce(
    (acc, job) => {

      acc[job.hospital] =
        (acc[job.hospital] || 0) + 1;

      return acc;

    },
    {}
  );

  const hospitalData =
    Object.entries(jobsByHospital)
      .map(([hospital, value]) => ({
        hospital,
        value
      }))
      .sort(
        (a, b) =>
          b.value - a.value
      );

  return (
    <div
      style={{
        padding: 24,
        maxWidth: 1200,
        margin: "0 auto"
      }}
    >

      {/* KPI Cards */}

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-between",
          marginBottom: 24
        }}
      >
        <MetricCard
          title="Total Jobs"
          value={totalJobs}
          detail="All hospital listings"
        />

        <MetricCard
          title="Hospital Count"
          value={
            Object.keys(
              jobsByHospital
            ).length
          }
          detail="Unique hospital sources"
        />

        <MetricCard
          title="Top Hospital"
          value={
            hospitalData[0]?.hospital ||
            "N/A"
          }
          detail={
            `${hospitalData[0]?.value || 0} jobs`
          }
        />
      </div>

      {/* Hospital Chart */}

      <div
        style={{
          background: "#ffffff",
          borderRadius: 16,
          padding: 24,
          boxShadow:
            "0 2px 12px rgba(0,0,0,0.06)"
        }}
      >
        <h2>
          Jobs by Hospital
        </h2>

        <ResponsiveContainer
          width="100%"
          height={300}
        >
          <BarChart
            data={hospitalData}
          >
            <XAxis
              dataKey="hospital"
            />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey="value"
              fill="#2563eb"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Location Chart */}

      <div
        style={{
          background: "#ffffff",
          borderRadius: 16,
          padding: 24,
          marginTop: 24,
          boxShadow:
            "0 2px 12px rgba(0,0,0,0.06)"
        }}
      >
        <h2>
          Jobs by Location
        </h2>

        <ResponsiveContainer
          width="100%"
          height={350}
        >
          <BarChart
            data={locationData}
          >
            <XAxis
              dataKey="location"
            />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey="value"
              fill="#10b981"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
       <div
  style={{
    background: "#ffffff",
    borderRadius: 16,
    padding: 24,
    marginTop: 24,
    boxShadow:
      "0 2px 12px rgba(0,0,0,0.06)"
  }}
>
  <h2>
    Top Departments
  </h2>

  <ResponsiveContainer
    width="100%"
    height={350}
  >
    <BarChart
      data={departmentData}
    >
      <XAxis
        dataKey="department"
      />

      <YAxis />

      <Tooltip />

      <Bar
        dataKey="value"
        fill="#f59e0b"
      />
    </BarChart>
  </ResponsiveContainer>
</div>
      {/* Recent Jobs */}

      <div
        style={{
          marginTop: 24
        }}
      >
        <h2>
          Recent Jobs
        </h2>

        <JobTable
          jobs={jobs.slice(0, 20)}
        />
      </div>

    </div>
  );
}

export default HomePage;