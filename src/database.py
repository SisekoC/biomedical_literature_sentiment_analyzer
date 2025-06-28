from sqlalchemy import create_engine

# Replace with your actual DB credentials
DATABASE_URL = "postgresql+psycopg2://postgres:Sc970928@localhost:5432/literature_db"

engine = create_engine(DATABASE_URL)
