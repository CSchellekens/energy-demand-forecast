from typing import Any

import pandas as pd

from .api_client import ApiClient
from .base import DataSource

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


class OpenMetoTemperature(DataSource):
    name = "Temperature"

    def __init__(self, latitude: float = 52.10, longitude: float = 5.18) -> None:
        self.client = ApiClient(
            base_url=ARCHIVE_URL,
            default_params={
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "temperature_2m",
                "timezone": "UTC",
            },
        )

    def _download(self, start: str, end: str) -> Any:
        return self.client.get(start_date=start, end_date=end)

    def _to_frame(self, raw: Any) -> pd.DataFrame:
        hourly = raw["hourly"]
        df = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(hourly["time"], utc=True),
                "temperature": hourly["temperature_2m"],
            }
        )
        return df.set_index("timestamp")
