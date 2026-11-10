"""Opslaan van een data source door het te dependency te injecten in een cached source class."""

from pathlib import Path

import pandas as pd

from .base import DataSource


class CachedSource:
    def __init__(self, source: DataSource, cache_dir: Path = Path("data/raw")) -> None:
        self.source = source
        self.cache_dir = cache_dir

    @property
    def name(self) -> str:
        return self.source.name

    def fetch(self, start: str, end: str) -> pd.DataFrame:
        path = self.cache_dir / f"{self.name}_{start}_{end}.parquet"
        if path.exists():
            return pd.read_parquet(path)
        df = self.source.fetch(start, end)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path)
        return df
