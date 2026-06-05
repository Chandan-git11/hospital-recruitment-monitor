import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.services.database import JobDatabase

db = JobDatabase("data/jobs.db")

print("Total Jobs:", db.count_jobs())

jobs = db.fetch_all()

print("\nFirst 5 Jobs\n")

for job in jobs[:5]:
    print(job)
    print("-" * 80)