from .sources.cache import CachedSource
from .sources.entsoe import EntsoeData
from .sources.open_meteo import OpenMeteoTemperature

START = "2023-01-01"
END = "2026-11-11"


def main() -> None:
    sources = [CachedSource(OpenMeteoTemperature()), CachedSource(EntsoeData())]
    for source in sources:
        df = source.fetch(START, END)
        print(f"{source.name}: {len(df)} rijen, {df.index.min()} tot {df.index.max()}")


if __name__ == "__main__":
    main()
