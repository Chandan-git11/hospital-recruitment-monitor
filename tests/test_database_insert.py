import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.parsers.fortis_parser import FortisParser
from scraper.services.database import JobDatabase

parser = FortisParser()

jobs = parser.fetch_jobs()

print(f"\nFetched {len(jobs)} jobs")

db = JobDatabase("data/jobs.db")

db.create_tables()

db.insert_jobs(jobs)

print("Jobs inserted successfully")

print("Total jobs in database:", db.count_jobs())