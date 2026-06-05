from .generic_parser import GenericParser


class ApolloParser(GenericParser):
    def parse(self, html: str, hospital: str) -> list[dict]:
        jobs = super().parse(html, hospital)
        for job in jobs:
            if not job["job_type"]:
                job["job_type"] = "Full-time"
        return jobs
