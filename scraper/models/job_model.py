# scraper/models/job_model.py

from dataclasses import dataclass


@dataclass
class JobPost:
    """
    Standard job schema used across all hospital parsers.
    """

    title: str
    location: str
    department: str
    job_type: str
    posted_date: str
    url: str
    hospital: str

    def to_dict(self) -> dict:
        """
        Convert JobPost object to dictionary.
        """
        return {
            "title": self.title,
            "location": self.location,
            "department": self.department,
            "job_type": self.job_type,
            "posted_date": self.posted_date,
            "url": self.url,
            "hospital": self.hospital,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create JobPost object from dictionary.
        """
        return cls(
            title=data.get("title", ""),
            location=data.get("location", ""),
            department=data.get("department", ""),
            job_type=data.get("job_type", ""),
            posted_date=data.get("posted_date", ""),
            url=data.get("url", ""),
            hospital=data.get("hospital", ""),
        )

    def __str__(self) -> str:
        return (
            f"JobPost("
            f"title='{self.title}', "
            f"hospital='{self.hospital}', "
            f"location='{self.location}')"
        )