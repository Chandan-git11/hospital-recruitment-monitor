import time
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..core.config import SCRAPER_INTERVAL_MINUTES
from ..logger import configure_logger

logger = configure_logger().getChild("scheduler")


class ScraperScheduler:
    def __init__(self, task: Callable[[], None]):
        self.task = task
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        trigger = IntervalTrigger(minutes=SCRAPER_INTERVAL_MINUTES)
        self.scheduler.add_job(
            self.task,
            trigger=trigger,
            id="hospital_career_scraper",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        self.scheduler.start()
        logger.info("Scheduler started: interval=%s minutes", SCRAPER_INTERVAL_MINUTES)

        try:
            while True:
                time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler shutdown requested")
            self.scheduler.shutdown()


def run_scheduler() -> None:
    from ..main import run_scraper

    scheduler = ScraperScheduler(run_scraper)
    scheduler.start()
