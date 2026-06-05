from pathlib import Path
import pandas as pd

from ..core.config import EXPORT_DIR
from .database import JobDatabase


class JobExporter:
    def __init__(self, database: JobDatabase):
        self.database = database
        self.output_dir = Path(EXPORT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_all(self) -> None:
        jobs = self.database.fetch_all()
        if not jobs:
            return

        df = pd.DataFrame(jobs)
        csv_path = self.output_dir / "jobs.csv"
        xlsx_path = self.output_dir / "jobs.xlsx"
        df.to_csv(csv_path, index=False, encoding="utf-8")
        df.to_excel(xlsx_path, index=False)
