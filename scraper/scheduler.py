import time
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from scraper.core.config import SCRAPER_INTERVAL_MINUTES
from scraper.logger import configure_logger

logger = configure_logger().getChild("scheduler")


class ScraperScheduler:

    def __init__(self, task: Callable[[], None]):
        self.task = task
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:

        trigger = IntervalTrigger(
            minutes=SCRAPER_INTERVAL_MINUTES
        )

        self.scheduler.add_job(
            self.task,
            trigger=trigger,
            id="hospital_career_scraper",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

        logger.info(
            "Scheduler started. Interval=%s minutes",
            SCRAPER_INTERVAL_MINUTES
        )

        # Run immediately
        self.task()

        self.scheduler.start()

        try:
            while True:
                time.sleep(10)

        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler shutdown requested")
            self.scheduler.shutdown()