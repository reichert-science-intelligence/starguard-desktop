"""
Create synthetic sentiment corpus for CAHPS measure prediction.
Run: python -m data.create_sentiment_corpus
Output: data/sentiment_corpus.csv
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

SENTIMENT_SCENARIOS = {
    "Getting Care Quickly": [
        "I've been waiting 3 weeks for an appointment with my specialist.",
        "The urgent care was amazing - seen in 15 minutes!",
        "Called 5 times about my prescription, still no callback.",
    ],
    "Customer Service": [
        "The representative was rude and hung up on me.",
        "Sarah in member services solved my problem in one call!",
        "I've been on hold for 45 minutes trying to check my benefits.",
    ],
    "Care Coordination": [
        "Nobody told me I needed prior auth - now I'm stuck with a $2000 bill.",
        "The care coordinator helped me schedule all my appointments.",
        "My PCP never received the specialist notes.",
    ],
    "Health Plan Information": [
        "The benefit booklet is 200 pages - I can't find anything!",
        "The mobile app made it easy to find in-network providers.",
        "I didn't know I had OTC benefits until my neighbor told me.",
    ],
}


def generate_sentiment_data(n_records: int = 1000) -> pd.DataFrame:
    records = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=90)

    for i in range(n_records):
        member_id = f"MEM{random.randint(10000, 99999)}"
        cahps_category = random.choice(list(SENTIMENT_SCENARIOS.keys()))
        transcript = random.choice(SENTIMENT_SCENARIOS[cahps_category])

        # Sentiment score: -1 (negative) to +1 (positive)
        if any(w in transcript for w in ("amazing", "solved", "easy")):
            sentiment_score = random.uniform(0.6, 1.0)
            predicted_cahps = random.randint(9, 10)
        elif any(w in transcript for w in ("waiting", "rude", "stuck")):
            sentiment_score = random.uniform(-1.0, -0.4)
            predicted_cahps = random.randint(1, 5)
        else:
            sentiment_score = random.uniform(-0.3, 0.5)
            predicted_cahps = random.randint(6, 8)

        days_offset = random.randint(0, 90)
        call_date = start_date + timedelta(days=days_offset)

        records.append({
            "member_id": member_id,
            "call_date": call_date.isoformat(),
            "cahps_category": cahps_category,
            "transcript": transcript,
            "sentiment_score": round(sentiment_score, 3),
            "predicted_cahps_rating": predicted_cahps,
            "call_duration_seconds": random.randint(120, 1800),
            "agent_id": f"AGT{random.randint(100, 999)}",
        })

    return pd.DataFrame(records)


def main():
    script_dir = Path(__file__).parent
    output_path = script_dir / "sentiment_corpus.csv"
    df = generate_sentiment_data(1000)
    df.to_csv(output_path, index=False)
    print(f"Created {len(df)} sentiment records at {output_path}")


if __name__ == "__main__":
    main()
