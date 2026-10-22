import os
from dotenv import load_dotenv

load_dotenv()


def get_census_api_key() -> str:
    """Get the Census API key from environment variables."""
    census_api_key = os.getenv("CENSUS_API_KEY")
    if not census_api_key:
        raise ValueError("CENSUS_API_KEY is not set. Add it to your .env file (see .env.example).")
    return census_api_key
