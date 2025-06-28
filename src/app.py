import streamlit as st
import pandas as pd

# Import your existing modules
from sentiment_dashboard import plot_sentiment_dashboard
from topic_hype_indicator import plot_topic_hype
from trend_map import generate_interactive_trend_map

# Load data (you can adjust the path to your CSV or database query)
@st.cache_data
def load_data():
    # Example: replace with your data loading logic
    return pd.read_csv("output/articles_with_sentiment.csv")

def main():
    st.title("Biomedical Literature Sentiment Analyzer 📚🧠")

    # Dropdown selector
    option = st.selectbox(
        "Select visualization:",
        ("Sentiment Dashboard", "Topic Hype Indicator", "Trend Map")
    )

    # Load data
    df = load_data()

    # Render selected visualization
    if option == "Sentiment Dashboard":
        st.subheader("📊 Sentiment Dashboard")
        plot_sentiment_dashboard(df)

    elif option == "Topic Hype Indicator":
        st.subheader("🚀 Topic Hype Indicator")
        plot_topic_hype(df)

    elif option == "Trend Map":
        st.subheader("🗺️ Trend Map")
        generate_interactive_trend_map(df)

if __name__ == "__main__":
    main()
