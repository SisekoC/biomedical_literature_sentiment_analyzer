from sqlalchemy.orm import sessionmaker
from models import Article
from database import engine
from sentiment import analyze_sentiment

Session = sessionmaker(bind=engine)
session = Session()

# Fetch articles missing sentiment
articles = session.query(Article).filter(Article.sentiment_score == None).all()
print(f"Found {len(articles)} articles to update.")

for article in articles:
    if article.abstract:
        score = analyze_sentiment(article.abstract)
        article.sentiment_score = score
    else:
        article.sentiment_score = 0.0  # or None if you prefer

session.commit()
print("✅ Sentiment scores updated!")
