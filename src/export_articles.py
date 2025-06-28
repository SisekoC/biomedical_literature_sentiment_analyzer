import pandas as pd
from sqlalchemy import create_engine

# 🔑 Update this connection string if your DB details are different
engine = create_engine("postgresql+psycopg2://postgres:Sc970928@localhost:5432/literature_db")

def export_articles_with_sentiment():
    query = "SELECT * FROM articles;"
    df = pd.read_sql(query, engine)
    
    # Ensure output directory exists
    import os
    os.makedirs("output", exist_ok=True)
    
    output_path = "output/articles_with_sentiment.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Exported {len(df)} articles to {output_path}")

if __name__ == "__main__":
    export_articles_with_sentiment()
