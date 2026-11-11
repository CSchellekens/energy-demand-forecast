from pathlib import Path
from typing import Any

import pandas as pd

from .base import DataSource

FOLDER_NAME = Path("data/raw/entsoe")


class EntsoeData(DataSource):
    def __init__(self) -> None:
        self.name = "ActualTotalLoad"
        self.path = Path(FOLDER_NAME)

    def _download(self, start: str, end: str) -> Any:
        first = pd.Timestamp(start).to_period("M")
        last = pd.Timestamp(end).to_period("M")

        dfs = []
        for file in sorted(self.path.glob("*_ActualTotalLoad_*.csv")):
            month = pd.Period(file.name[:7].replace("_", "-"), freq="M")
            if first <= month <= last:
                df = pd.read_csv(file, sep="\t")
                dfs.append(df[df["AreaMapCode"] == "NL"])
        if len(dfs) == 0:
            raise FileNotFoundError(
                f"Geen ENTSOE bestanden gevonden voor {start} tot {end} in {self.path}"
            )
        return pd.concat(dfs, ignore_index=True)

    def _to_frame(self, raw: Any) -> pd.DataFrame:
        df = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(raw["DateTime(UTC)"], utc=True),
                "TotalLoad[MW]": raw["TotalLoad[MW]"],
            }
        )
        return df.set_index("timestamp")
