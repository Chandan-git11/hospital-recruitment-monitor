import json
from datetime import datetime

import requests

from scraper.core.config import DATA_DIR


class MaxParser:

    API_URL = (
        "https://maxhealthcarecareers.peoplestrong.com"
        "/api/cp/rest/altone/cp/jobs/v1"
    )

    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://maxhealthcarecareers.peoplestrong.com",
        "Referer": (
            "https://maxhealthcarecareers.peoplestrong.com/"
            "job/joblist"
        ),
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    HOSPITAL_NAME = "Max Healthcare"

    def fetch_jobs(self):

        jobs = []

        offset = 0
        limit = 45

        while True:

            payload = {
                "offset": offset,
                "limit": limit
            }

            try:

                response = requests.post(
                    self.API_URL,
                    json=payload,
                    headers=self.HEADERS,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                records = data.get(
                    "response",
                    []
                )

                if not records:
                    break

                print(
                    f"Fetched {len(records)} jobs "
                    f"(offset={offset})"
                )

                for item in records:

                    jobs.append(
                        {
                            "hospital": self.HOSPITAL_NAME,
                            "title": item.get(
                                "jobTitle",
                                ""
                            ),
                            "location": item.get(
                                "locationHierarchy",
                                ""
                            ),
                            "department": item.get(
                                "organizationUnit",
                                ""
                            ),
                            "job_type": "",
                            "posted_date": item.get(
                                "jobPostedDate",
                                ""
                            ),
                            "url": item.get(
                                "jobDetailUrl",
                                ""
                            )
                        }
                    )

                total_records = data.get(
                    "totalRecords",
                    0
                )

                offset += limit

                if offset >= total_records:
                    break

            except Exception as e:

                print(
                    f"Max fetch error: {e}"
                )

                break

        self.save_backup(jobs)

        print(
            f"\nTotal Max jobs collected: "
            f"{len(jobs)}"
        )

        return jobs

    def save_backup(self, jobs):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = (
            DATA_DIR
            / f"max_{timestamp}.json"
        )

        with open(
            backup_file,
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
            f"Backup saved: {backup_file}"
        )


if __name__ == "__main__":

    parser = MaxParser()

    jobs = parser.fetch_jobs()

    print(
        f"\nTotal jobs: {len(jobs)}"
    )

    if jobs:

        print("\nFirst Job:\n")

        print(
            json.dumps(
                jobs[0],
                indent=2,
                ensure_ascii=False
            )
        )