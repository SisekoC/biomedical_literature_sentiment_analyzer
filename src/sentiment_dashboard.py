import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_sentiment_dashboard(df):
    # Sentiment by Year
    fig1, ax1 = plt.subplots()
    yearly = df.groupby(df["publication_date"].str[:4]).sentiment_score.mean().reset_index()
    sns.lineplot(data=yearly, x="publication_date", y="sentiment_score", ax=ax1)
    ax1.set_title("Average Sentiment by Year")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Sentiment Score")
    st.pyplot(fig1)

    # Sentiment by Journal
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    journal = df.groupby("journal").sentiment_score.mean().sort_values().tail(10).reset_index()
    sns.barplot(data=journal, y="journal", x="sentiment_score", ax=ax2)
    ax2.set_title("Top 10 Journals by Average Sentiment")
    ax2.set_xlabel("Sentiment Score")
    ax2.set_ylabel("Journal")
    st.pyplot(fig2)

    # Sentiment Distribution
    fig3, ax3 = plt.subplots()
    sns.histplot(df.sentiment_score, bins=30, kde=True, ax=ax3)
    ax3.set_title("Sentiment Score Distribution")
    ax3.set_xlabel("Sentiment Score")
    st.pyplot(fig3)
