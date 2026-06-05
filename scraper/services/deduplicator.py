from typing import Iterable


def unique_jobs(jobs: Iterable[dict]) -> list[dict]:
    seen = set()
    unique_list = []
    for job in jobs:
        fingerprint = (job.get("title"), job.get("location"), job.get("department"), job.get("url"))
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        unique_list.append(job)
    return unique_list
