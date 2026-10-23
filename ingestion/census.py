import duckdb
import pandas as pd
import requests

from ingestion.config import (
    CENSUS_BASE_URL,
    CENSUS_DATASET,
    CENSUS_VARIABLES,
    CENSUS_YEAR,
    DUCKDB_PATH,
    RAW_PLACES_TABLE,
    REQUEST_TIMEOUT_SECONDS,
    get_census_api_key,
)


def fetch_places() -> list[list[str]]:
    """Fetch ACS data for every place in the US."""
    url = f"{CENSUS_BASE_URL}/{CENSUS_YEAR}/{CENSUS_DATASET}"
    columns = ",".join(["NAME", *CENSUS_VARIABLES.keys()])
    params = {
        "get": columns,
        "for": "place:*",
        "in": "state:*",
        "key": get_census_api_key(),
    }
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def load_places(rows: list[list[str]]) -> None:
    """Replace the raw places table with freshly fetched rows"""
    header, *data = rows
    places_df = pd.DataFrame(data, columns=header)
    with duckdb.connect(DUCKDB_PATH) as connection:
        connection.execute(f"CREATE OR REPLACE TABLE {RAW_PLACES_TABLE} AS SELECT * FROM places_df")


if __name__ == "__main__":
    load_places(fetch_places())
    with duckdb.connect(DUCKDB_PATH) as connection:
        print(connection.execute(f"SELECT count(*) FROM {RAW_PLACES_TABLE}").fetchone())
