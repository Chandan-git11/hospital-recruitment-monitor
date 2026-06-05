from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup


class GenericParser(ABC):
    @abstractmethod
    def parse(self, html: str, hospital: str) -> List[dict]:
        raise NotImplementedError

    def _clean_text(self, element) -> str:
        if not element:
            return ""
        return " ".join(element.get_text(separator=" ", strip=True).split())

    def _extract_job_url(self, element, hospital: str) -> str:
        link = element.select_one("a[href]")
        if link and link.get("href"):
            return link["href"].strip()
        return ""

    def _extract_job_card(self, element, hospital: str) -> dict:
        title = self._clean_text(element.select_one("h2, h3, .job-title, .title"))
        location = self._clean_text(element.select_one(".location, .job-location, .city, .meta-location"))
        department = self._clean_text(element.select_one(".department, .job-department, .team, .function"))
        job_type = self._clean_text(element.select_one(".job-type, .type, .employment-type"))
        posted_date = self._clean_text(element.select_one(".posted-date, .publish-date, .date, time"))
        url = self._extract_job_url(element, hospital)

        if not title and element.name == "a":
            title = self._clean_text(element)
        if not url and element.name == "a" and element.get("href"):
            url = element["href"].strip()

        return {
            "hospital": hospital,
            "title": title,
            "location": location,
            "department": department,
            "job_type": job_type,
            "posted_date": posted_date,
            "url": url,
        }

    def _find_job_blocks(self, soup: BeautifulSoup) -> List:
        selectors = [
            ".job-card",
            ".job-listing",
            ".jobItem",
            ".career-item",
            "article",
            "li",
            "div.card",
        ]
        blocks = []
        for selector in selectors:
            blocks = soup.select(selector)
            if len(blocks) >= 3:
                return blocks
        return soup.select("div")[:20]

    def parse(self, html: str, hospital: str) -> List[dict]:
        soup = BeautifulSoup(html, "html.parser")
        job_blocks = self._find_job_blocks(soup)
        jobs = []

        for block in job_blocks:
            job = self._extract_job_card(block, hospital)
            if job["title"] and job["url"]:
                jobs.append(job)

        return jobs


class DefaultParser(GenericParser):
    def parse(self, html: str, hospital: str) -> List[dict]:
        return super().parse(html, hospital)
