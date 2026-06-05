import sys
from pathlib import Path
import tempfile

print("STARTING TEST...")

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

print("ROOT PATH ADDED")

from scraper.services.database import JobDatabase

print("DATABASE IMPORTED")


def test_database_insert_and_fetch():

    print("RUNNING TEST FUNCTION")

    with tempfile.TemporaryDirectory() as tmpdir:

        db_path = Path(tmpdir) / "jobs.db"

        print("DB PATH:", db_path)

        db = JobDatabase(db_path)

        print("DB OBJECT CREATED")

        db.create_tables()

        print("TABLE CREATED")

        jobs = [
            {
                "title": "Test Nurse",
                "location": "Delhi",
                "department": "Nursing",
                "job_type": "Full-time",
                "posted_date": "2026-05-28",
                "url": "https://example.com/job-1",
                "hospital": "apollo",
            }
        ]

        db.insert_jobs(jobs)

        print("JOB INSERTED")

        results = db.fetch_all()

        print("RESULTS:", results)

        assert len(results) == 1

        print("TEST PASSED")


if __name__ == "__main__":
    test_database_insert_and_fetch()
    