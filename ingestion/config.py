import os

from dotenv import load_dotenv

load_dotenv()

CENSUS_BASE_URL = "https://api.census.gov/data"
CENSUS_YEAR = 2024
CENSUS_DATASET = "acs/acs5"
CENSUS_VARIABLES = {
    "B01003_001E": "total_population",
    "B19013_001E": "median_household_income",
    "B25064_001E": "median_gross_rent",
    "B25077_001E": "median_home_value",
}
REQUEST_TIMEOUT_SECONDS = 30


def get_census_api_key() -> str:
    """Get the Census API key from environment variables."""
    census_api_key = os.getenv("CENSUS_API_KEY")
    if not census_api_key:
        raise ValueError("CENSUS_API_KEY is not set. Add it to your .env file (see .env.example).")
    return census_api_key
