# scraper/main.py

import argparse

from scraper.core.config import DATABASE_PATH
from scraper.logger import configure_logger
from scraper.utils import ensure_data_directories

from scraper.services.database import JobDatabase

from scraper.parsers.fortis_parser import FortisParser
from scraper.parsers.manipal_parser import ManipalParser
from scraper.parsers.max_parser import MaxParser


logger = configure_logger()


def run_scraper() -> None:

    ensure_data_directories()

    logger.info(
        "Starting hospital career scraping pipeline"
    )

    db = JobDatabase(DATABASE_PATH)

    db.create_tables()

    all_jobs = []

    # =========================
    # FORTIS
    # =========================

    try:

        logger.info(
            "Fetching Fortis jobs..."
        )

        fortis_jobs = (
            FortisParser()
            .fetch_jobs()
        )

        logger.info(
            f"Extracted {len(fortis_jobs)} jobs for Fortis"
        )

        all_jobs.extend(
            fortis_jobs
        )

    except Exception as e:

        logger.exception(
            f"Fortis scraper failed: {e}"
        )

    # =========================
    # MANIPAL
    # =========================

    try:

        logger.info(
            "Fetching Manipal jobs..."
        )

        manipal_jobs = (
            ManipalParser()
            .fetch_jobs()
        )

        logger.info(
            f"Extracted {len(manipal_jobs)} jobs for Manipal"
        )

        all_jobs.extend(
            manipal_jobs
        )

    except Exception as e:

        logger.exception(
            f"Manipal scraper failed: {e}"
        )

    # =========================
    # MAX HEALTHCARE
    # =========================

    try:

        logger.info(
            "Fetching Max Healthcare jobs..."
        )

        max_jobs = (
            MaxParser()
            .fetch_jobs()
        )

        logger.info(
            f"Extracted {len(max_jobs)} jobs for Max Healthcare"
        )

        all_jobs.extend(
            max_jobs
        )

    except Exception as e:

        logger.exception(
            f"Max Healthcare scraper failed: {e}"
        )

    # =========================
    # DATABASE INSERT
    # =========================

    if not all_jobs:

        logger.warning(
            "No jobs collected."
        )

        return

    inserted = db.insert_jobs(
        all_jobs
    )

    logger.info(
        f"Total jobs fetched: {len(all_jobs)}"
    )

    logger.info(
        f"New jobs inserted: {inserted}"
    )

    logger.info(
        f"Total jobs in database: {db.count_jobs()}"
    )

    logger.info(
        "Scraper pipeline completed"
    )


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Hospital Career Monitor"
    )

    parser.add_argument(
        "--run",
        action="store_true",
        help="Run scraper once"
    )

    parser.parse_args()

    run_scraper()


if __name__ == "__main__":
    main()