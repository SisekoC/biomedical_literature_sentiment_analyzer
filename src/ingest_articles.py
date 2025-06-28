

import json
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Article, Sentiment, Topic
from textblob import TextBlob
from dotenv import load_dotenv

# --- Load environment variables from .env if available ---
load_dotenv()

# --- Config Variables (use environment or fallback defaults) ---
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Sc970928")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "literature_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- File Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "pubmed" / "pubmed_abstracts.jsonl"

# --- Database Setup ---
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# --- NLP Placeholder Functions ---
def analyze_sentiment(text):
    if not text:
        return 0.0, 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def extract_topics(text):
    if not text:
        return "N/A", 0.0
    return "biomedical", 1.0  # placeholder logic

# --- Main Function ---
def ingest_articles():
    session = Session()

    if not DATA_FILE.exists():
        print(f"❌ Data file not found: {DATA_FILE}")
        return

    print(f"📖 Reading: {DATA_FILE}")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)

            # Skip duplicates based on PMID
            if session.query(Article).filter_by(pmid=item["pmid"]).first():
                print(f"🔁 Skipping duplicate PMID: {item['pmid']}")
                continue

            article = Article(
                pmid=item["pmid"],
                title=item.get("title"),
                abstract=item.get("abstract"),
                journal=item.get("journal"),
                authors=item.get("authors"),
                publication_date=item.get("publication_date"),
                source=item.get("source", "pubmed"),
                sentiment_score=analyze_sentiment(item["abstract"]),
            )

            polarity, subjectivity = analyze_sentiment(item.get("abstract", ""))
            sentiment = Sentiment(
                polarity=polarity,
                subjectivity=subjectivity,
                model_version="textblob_v1",
            )
            article.sentiments.append(sentiment)

            topic_label, topic_score = extract_topics(item.get("abstract", ""))
            topic = Topic(
                topic_label=topic_label,
                score=topic_score,
                method="placeholder",
            )
            article.topics.append(topic)

            session.add(article)

    Base.metadata.create_all(engine)
    session.commit()
    session.close()
    print("✅ Ingest complete!")

# --- Entry Point ---
if __name__ == "__main__":
    ingest_articles()
