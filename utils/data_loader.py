"""
Data loader for HEDIS Portfolio Optimizer Phase 1 enhancements.
Loads sentiment corpus, SDoH mapping, and member data (DB or synthetic).
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Base path for data files
DATA_DIR = Path(__file__).parent.parent / "data"


def load_sentiment_corpus() -> pd.DataFrame:
    """Load sentiment corpus (call transcripts with CAHPS sentiment scores)."""
    path = DATA_DIR / "sentiment_corpus.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "call_date" in df.columns:
        df["call_date"] = pd.to_datetime(df["call_date"], errors="coerce")
    return df


def load_sdoh_mapping() -> pd.DataFrame:
    """Load SDoH mapping (ZIP code -> barrier scores)."""
    path = DATA_DIR / "sdoh_mapping.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_member_data_for_outreach() -> pd.DataFrame:
    """
    Load member data with columns needed for SDoH mapper and channel optimizer:
    member_id, zip_code, hedis_gap_count, age, tech_savvy_score, email_on_file, primary_barrier
    Tries DB first; falls back to synthetic data.
    """
    try:
        from data.db import query

        # Try to get members with gap counts from DB
        sql = """
        SELECT m.member_id, m.zip_code, m.age,
               COALESCE(g.gap_count, 0) as hedis_gap_count
        FROM members m
        LEFT JOIN (
            SELECT member_id, COUNT(*) as gap_count
            FROM gaps
            WHERE gap_status = 'open'
            GROUP BY member_id
        ) g ON m.member_id = g.member_id
        LIMIT 500
        """
        df = query(sql)
        if df is not None and not df.empty:
            # Add synthetic columns not in DB
            np.random.seed(42)
            n = len(df)
            df["tech_savvy_score"] = np.random.uniform(0.2, 0.95, n)
            df["email_on_file"] = np.random.choice([True, False], n, p=[0.6, 0.4])
            # primary_barrier will be joined from SDoH
            return df
    except Exception:
        pass

    # Fallback: synthetic member data
    np.random.seed(42)
    sdoh = load_sdoh_mapping()
    zip_codes = (
        sdoh["zip_code"].tolist()
        if not sdoh.empty
        else [f"{np.random.randint(10001, 99999)}" for _ in range(200)]
    )

    n_members = min(300, len(zip_codes) * 2)
    member_ids = [f"MEM{10000 + i}" for i in range(n_members)]
    ages = np.random.randint(45, 90, n_members)
    zips = np.random.choice(zip_codes, n_members, replace=True)
    gap_counts = np.random.randint(0, 5, n_members)
    tech_savvy = np.random.uniform(0.2, 0.95, n_members)
    email_on_file = np.random.choice([True, False], n_members, p=[0.6, 0.4])

    df = pd.DataFrame(
        {
            "member_id": member_ids,
            "zip_code": zips,
            "age": ages,
            "hedis_gap_count": gap_counts,
            "tech_savvy_score": tech_savvy,
            "email_on_file": email_on_file,
        }
    )
    return df


def get_merged_member_sdoh() -> pd.DataFrame:
    """Merge member data with SDoH mapping by zip_code. Adds primary_barrier, flags."""
    members = load_member_data_for_outreach()
    sdoh = load_sdoh_mapping()
    if members.empty or sdoh.empty:
        return members

    merged = members.merge(
        sdoh[["zip_code", "primary_barrier", "transit_access_score", "food_desert_score"]],
        on="zip_code",
        how="left",
        suffixes=("", "_sdoh"),
    )
    merged["primary_barrier"] = merged["primary_barrier"].fillna("None")
    merged["has_transport_barrier"] = merged["transit_access_score"] < 5
    merged["has_food_barrier"] = merged["food_desert_score"] > 6
    return merged


def get_member_sentiment_lookup() -> dict:
    """Return member_id -> avg sentiment_score from corpus (for agentic outreach)."""
    df = load_sentiment_corpus()
    if df.empty or "member_id" not in df.columns or "sentiment_score" not in df.columns:
        return {}
    return df.groupby("member_id")["sentiment_score"].mean().to_dict()
