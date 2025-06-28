import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# === CONFIG ===
DB_URL = "postgresql+psycopg2://postgres:Sc970928@localhost:5432/literature_db"  # Replace with your real credentials
engine = create_engine(DB_URL)

# === 1. Time-Based Sentiment Trends ===
with engine.connect() as conn:
    df_time = pd.read_sql(text("""
        SELECT
            DATE_TRUNC('month', publication_date) AS month,
            AVG(sentiment_score) AS avg_sentiment,
            COUNT(*) AS count
        FROM articles
        WHERE sentiment_score IS NOT NULL
        GROUP BY month
        ORDER BY month
    """), conn)
    print(df_time.head())  # or df.to_string()


plt.figure(figsize=(12, 6))
sns.lineplot(data=df_time, x="month", y="avg_sentiment", marker="o")
plt.title("📈 Average Sentiment Over Time")
plt.xlabel("Month")
plt.ylabel("Average Sentiment Score")
plt.grid(True)
plt.tight_layout()
plt.show()

# === 2. Journal-Based Sentiment Comparison ===
with engine.connect() as conn:
    df_journal = pd.read_sql(text("""
        SELECT
            journal,
            COUNT(*) AS count,
            AVG(sentiment_score) AS avg_sentiment
        FROM articles
        WHERE sentiment_score IS NOT NULL
        GROUP BY journal
        HAVING COUNT(*) > 10
        ORDER BY avg_sentiment DESC
        LIMIT 20
    """), conn)
    print(df_journal.head())  # or df.to_string()


plt.figure(figsize=(10, 6))
sns.barplot(data=df_journal, y="journal", x="avg_sentiment", palette="coolwarm")
plt.title("📰 Top Journals by Average Sentiment")
plt.xlabel("Average Sentiment")
plt.ylabel("Journal")
plt.tight_layout()
plt.show()

# === 3. Sentiment Polarity Distribution ===
with engine.connect() as conn:
    df_polarity = pd.read_sql(text("""
        SELECT
            CASE
                WHEN sentiment_score > 0.05 THEN 'Positive'
                WHEN sentiment_score < -0.05 THEN 'Negative'
                ELSE 'Neutral'
            END AS sentiment_category,
            COUNT(*) AS count
        FROM articles
        WHERE sentiment_score IS NOT NULL
        GROUP BY sentiment_category
    """), conn)
    print(df_polarity.head())  # or df.to_string()

plt.figure(figsize=(6, 6))
plt.pie(df_polarity['count'], labels=df_polarity['sentiment_category'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title("🧠 Sentiment Polarity Distribution")
plt.axis("equal")
plt.tight_layout()
plt.show()
