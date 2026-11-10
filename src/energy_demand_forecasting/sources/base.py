"""Abstracte base class voor het implementeren van
verschillende datasrouces die een gedeelde pipeline hebben."""

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


def validate(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Valideren van dataframes op het einde van de fetch-methode vd datasource ABC."""
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{name}: index moet een DateTimeIndex zijn")
    if df.index.tz is None or str(df.index.tz) != "UTC":
        raise ValueError(f"{name}: index moet in UTC zijn")
    if not df.index.is_unique:
        raise ValueError(f"{name}: dubbele tijdsindex")
    if df.empty:
        raise ValueError(f"{name}: geen data in df")
    return df.sort_index()


class DataSource(ABC):
    """Abstracten data classen om te beschrijven wat er moet gebeuren voor elke data bron."""

    name: str

    def fetch(self, start: str, end: str) -> pd.DataFrame:
        raw = self._download(start, end)
        df = self._to_frame(raw)
        return validate(df, self.name)

    @abstractmethod
    def _download(self, start: str, end: str) -> Any:
        """Abstract method voor het downloaden van data. is een prive functie"""

    @abstractmethod
    def _to_frame(self, raw: Any) -> pd.DataFrame:
        """Abstracte prive methode om de gedownloaden data omtezetten naar een dataframe"""
