import json
from pathlib import Path
from datetime import datetime

import requests


class ManipalParser:

    API_URL = "https://public.zwayam.com/jobs/search"

    HOSPITAL_NAME = "Manipal"

    DOMAIN = "careers.manipalhospitals.com"
    COMPANY_ID = "MTU1OTA="

    def fetch_jobs(self):

        jobs = []

        start = 0

        while True:

            filter_criteria = {
                "paginationStartNo": start,
                "selectedCall": "sort",
                "sortCriteria": {
                    "name": "modifiedDate",
                    "isAscending": False
                },
                "anyOfTheseWords": ""
            }

            payload = {
                "filterCri": json.dumps(filter_criteria),
                "domain": self.DOMAIN,
                "companyId": self.COMPANY_ID
            }

            headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",

                "Origin":
                "https://careers.manipalhospitals.com",

                "Referer":
                "https://careers.manipalhospitals.com/",

                "Content-Type":
                "application/x-www-form-urlencoded"
            }

            try:

                response = requests.post(
                    self.API_URL,
                    data=payload,
                    headers=headers,
                    timeout=30
                )

                response.raise_for_status()

                result = response.json()

                records = (
                    result.get("data", {})
                          .get("data", [])
                )

                if not records:
                    break

                for item in records:

                    source = item.get("_source", {})

                    title = (
                        source.get("jobTitle")
                        or source.get("designation")
                        or "Unknown"
                    )

                    location = source.get(
                        "officeLocation",
                        ""
                    )

                    department = source.get(
                        "departmentName",
                        ""
                    )

                    reference = source.get(
                        "referenceNumber",
                        ""
                    )

                    posted = source.get(
                        "modifiedDate",
                        ""
                    )

                    jobs.append({
                        "hospital": "Manipal",
                        "title": title,
                        "location": location,
                        "department": department,
                        "job_type": "",
                        "posted_date": posted,
                        "url":
                        f"https://careers.manipalhospitals.com/job/{reference}"
                    })

                print(
                    f"Fetched {len(records)} jobs "
                    f"(offset={start})"
                )

                start += len(records)

            except Exception as e:

                print(
                    f"Manipal fetch error: {e}"
                )

                break

        self.save_backup(jobs)

        print(
            f"\nTotal Manipal jobs collected: "
            f"{len(jobs)}"
        )

        return jobs

    def save_backup(self, jobs):

        raw_dir = Path("data/raw")

        raw_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        file_name = raw_dir / (
            f"manipal_{datetime.now():%Y%m%d_%H%M%S}.json"
        )

        with open(
            file_name,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                jobs,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Backup saved: {file_name}"
        )
        