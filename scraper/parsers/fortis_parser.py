
# scraper/parsers/fortis_parser.py

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import requests


class FortisParser:

    BASE_URL = (
        "https://fa-ermg-saasfaprod1.fa.ocs.oraclecloud.com/"
        "hcmRestApi/resources/latest/recruitingCEJobRequisitions"
    )

    HOSPITAL_NAME = "Fortis"

    def normalize_job(self, req: Dict) -> Dict:

        location = req.get("PrimaryLocation", "")

        if location and "," in location:
            location = location.split(",")[0].strip()

        job_id = req.get("Id", "")

        return {
            "hospital": self.HOSPITAL_NAME,
            "title": req.get("Title", "").strip(),
            "location": location,
            "department": req.get("Department", ""),
            "job_type": req.get("WorkerType", ""),
            "posted_date": req.get("PostedDate", ""),
            "url": (
                f"https://fortishealthcare.com/careers/job/{job_id}"
            ),
        }

    def save_raw_backup(self, jobs: List[Dict]) -> None:

        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)

        filename = raw_dir / (
            f"fortis_{datetime.now():%Y%m%d_%H%M%S}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                jobs,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"Backup saved: {filename}")

    def fetch_jobs(self) -> List[Dict]:

        jobs = []

        offset = 0
        limit = 25

        while True:

            params = {
                "onlyData": "true",
                "expand": (
                    "requisitionList.workLocation,"
                    "requisitionList.otherWorkLocations,"
                    "requisitionList.secondaryLocations,"
                    "flexFieldsFacet.values,"
                    "requisitionList.requisitionFlexFields"
                ),
                "finder": (
                    f"findReqs;"
                    f"siteNumber=CX_1,"
                    f"limit={limit},"
                    f"offset={offset},"
                    f"sortBy=POSTING_DATES_DESC"
                ),
            }

            try:

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    timeout=30,
                )

                response.raise_for_status()

                data = response.json()

                items = data.get("items", [])

                if not items:
                    break

                requisitions = items[0].get(
                    "requisitionList",
                    []
                )

                if not requisitions:
                    break

                normalized_jobs = [
                    self.normalize_job(req)
                    for req in requisitions
                ]

                jobs.extend(normalized_jobs)

                print(
                    f"Fetched {len(requisitions)} jobs "
                    f"(offset={offset})"
                )

                offset += limit

            except requests.RequestException as e:

                print(
                    f"Error fetching Fortis jobs: {e}"
                )

                break

        print(
            f"\nTotal Fortis jobs collected: {len(jobs)}"
        )

        self.save_raw_backup(jobs)

        return jobs

    def parse(
        self,
        html=None,
        hospital_name=None
    ) -> List[Dict]:
        """
        Compatibility method for JobExtractor.
        """
        return self.fetch_jobs()


if __name__ == "__main__":

    parser = FortisParser()

    jobs = parser.fetch_jobs()

    print("\nFirst Job:\n")

    if jobs:
        print(
            json.dumps(
                jobs[0],
                indent=2,
                ensure_ascii=False,
            )
        )

    print(f"\nTotal Jobs: {len(jobs)}")
