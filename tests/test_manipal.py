import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scraper.parsers.manipal_parser import ManipalParser

parser = ManipalParser()

jobs = parser.fetch_jobs()

print(f"\nTotal jobs: {len(jobs)}")

if jobs:
    print(jobs[0])