# scraper/services/database.py

import sqlite3
from pathlib import Path
from typing import Iterable

from ..models.job_model import JobPost


class JobDatabase:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    # =========================
    # TABLE CREATION
    # =========================

    def create_tables(self) -> None:
        conn = self._connect()

        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    hospital TEXT NOT NULL,
                    title TEXT NOT NULL,

                    location TEXT,
                    department TEXT,
                    job_type TEXT,

                    posted_date TEXT,

                    url TEXT NOT NULL UNIQUE,

                    is_new INTEGER DEFAULT 1,

                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS scrape_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    hospital TEXT NOT NULL,

                    jobs_found INTEGER DEFAULT 0,

                    status TEXT,

                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS ix_jobs_hospital
                ON jobs(hospital)
            """)

            conn.commit()

        finally:
            conn.close()

    # =========================
    # JOB INSERTION
    # =========================

    def job_exists(self, url: str) -> bool:
        conn = self._connect()

        try:
            cursor = conn.execute(
                "SELECT 1 FROM jobs WHERE url = ?",
                (url,)
            )

            return cursor.fetchone() is not None

        finally:
            conn.close()

    def insert_job(self, raw_job: dict) -> bool:
        """
        Returns:
            True  -> New job inserted
            False -> Job already existed
        """

        job = JobPost(
            title=raw_job.get("title", ""),
            location=raw_job.get("location", ""),
            department=raw_job.get("department", ""),
            job_type=raw_job.get("job_type", ""),
            posted_date=raw_job.get("posted_date", ""),
            url=raw_job.get("url", ""),
            hospital=raw_job.get("hospital", ""),
        )

        if not job.url:
            return False

        conn = self._connect()

        try:
            cursor = conn.execute("""
                INSERT OR IGNORE INTO jobs (
                    hospital,
                    title,
                    location,
                    department,
                    job_type,
                    posted_date,
                    url,
                    is_new
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.hospital,
                job.title,
                job.location,
                job.department,
                job.job_type,
                job.posted_date,
                job.url,
                1
            ))

            conn.commit()

            return cursor.rowcount > 0

        finally:
            conn.close()

    def insert_jobs(self, jobs: Iterable[dict]) -> int:
        self.create_tables()

        inserted_count = 0

        for job in jobs:
            if self.insert_job(job):
                inserted_count += 1

        return inserted_count

    # =========================
    # FETCH JOBS
    # =========================

    def fetch_all(self) -> list[dict]:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT
                    hospital,
                    title,
                    location,
                    department,
                    job_type,
                    posted_date,
                    url,
                    is_new,
                    scraped_at
                FROM jobs
                ORDER BY scraped_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    def fetch_by_hospital(self, hospital_name: str) -> list[dict]:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT
                    hospital,
                    title,
                    location,
                    department,
                    job_type,
                    posted_date,
                    url,
                    is_new,
                    scraped_at
                FROM jobs
                WHERE LOWER(hospital)=LOWER(?)
                ORDER BY scraped_at DESC
            """,
            (hospital_name.strip(),))

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    def fetch_new_jobs(self) -> list[dict]:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT *
                FROM jobs
                WHERE is_new = 1
                ORDER BY scraped_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    # =========================
    # COUNTS & ANALYTICS
    # =========================

    def count_jobs(self) -> int:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT COUNT(*) AS total
                FROM jobs
            """)

            row = cursor.fetchone()

            return int(row["total"])

        finally:
            conn.close()

    def jobs_added_today(self) -> int:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT COUNT(*) AS total
                FROM jobs
                WHERE DATE(scraped_at)=DATE('now')
            """)

            row = cursor.fetchone()

            return int(row["total"])

        finally:
            conn.close()

    def jobs_by_hospital(self) -> list[dict]:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT
                    hospital,
                    COUNT(*) AS total_jobs
                FROM jobs
                GROUP BY hospital
                ORDER BY total_jobs DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    def jobs_by_department(self) -> list[dict]:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT
                    department,
                    COUNT(*) AS total_jobs
                FROM jobs
                GROUP BY department
                ORDER BY total_jobs DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    # =========================
    # SCRAPE LOGS
    # =========================

    def insert_scrape_log(
        self,
        hospital: str,
        jobs_found: int,
        status: str,
        started_at: str,
        completed_at: str,
    ) -> None:

        conn = self._connect()

        try:
            conn.execute("""
                INSERT INTO scrape_logs (
                    hospital,
                    jobs_found,
                    status,
                    started_at,
                    completed_at
                )
                VALUES (?, ?, ?, ?, ?)
            """,
            (
                hospital,
                jobs_found,
                status,
                started_at,
                completed_at,
            ))

            conn.commit()

        finally:
            conn.close()

    def fetch_scrape_logs(self) -> list[dict]:
        conn = self._connect()

        try:
            cursor = conn.execute("""
                SELECT *
                FROM scrape_logs
                ORDER BY id DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    # =========================
    # MAINTENANCE
    # =========================

    def mark_all_jobs_old(self) -> None:
        """
        Optional:
        Run before a new scrape if you want only
        newly discovered jobs to have is_new=1.
        """

        conn = self._connect()

        try:
            conn.execute("""
                UPDATE jobs
                SET is_new = 0
            """)

            conn.commit()

        finally:
            conn.close()