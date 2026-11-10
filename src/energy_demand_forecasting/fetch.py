from .sources.cache import CachedSource
from .sources.open_meteo import OpenMeteoTemperature

START = "2023-01-01"
END = "2025-12-31"


def main() -> None:
    sources = [CachedSource(OpenMeteoTemperature())]
    for source in sources:
        df = source.fetch(START, END)
        print(f"{source.name}: {len(df)} rijen, {df.index.min()} tot {df.index.max()}")


if __name__ == "__main__":
    main()
