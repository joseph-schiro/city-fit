import duckdb
import pandas as pd
import streamlit as st

from ingestion.config import DUCKDB_PATH

SCORE_COLUMNS = {
    "rent_score": "Rent affordability",
    "home_price_score": "Home affordability",
    "income_score": "Income",
}


@st.cache_data
def load_scores() -> pd.DataFrame:
    """Load the city scores mart from DuckDB."""
    with duckdb.connect(DUCKDB_PATH, read_only=True) as connection:
        return connection.execute("SELECT * FROM fct_city_scores").df()


def main() -> None:
    st.title("CityFit")
    scores_df = load_scores()

    st.sidebar.header("What matters to you?")
    weights = {
        column: st.sidebar.slider(label, 0, 10, 5) for column, label in SCORE_COLUMNS.items()
    }
    total_weight = sum(weights.values()) or 1

    scores_df["fit_score"] = (
        sum(scores_df[column] * weight for column, weight in weights.items()) / total_weight
    )
    ranked_df = scores_df.sort_values("fit_score", ascending=False)

    st.dataframe(ranked_df[["place_name", "fit_score", *SCORE_COLUMNS]], hide_index=True)


main()
