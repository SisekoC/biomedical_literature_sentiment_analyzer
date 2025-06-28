# src/sentiment.py

from textblob import TextBlob

def analyze_sentiment(text: str) -> float:
    """
    Analyze sentiment of a given text using TextBlob.
    Returns a sentiment polarity score between -1.0 (very negative) and 1.0 (very positive).
    """
    if not text or not text.strip():
        return 0.0  # Neutral for empty or missing text
    
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 4)
