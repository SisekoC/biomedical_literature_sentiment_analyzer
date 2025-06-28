import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_topic_hype(df):
    # Example: frequency of top words over time (replace with your actual NLP topic extraction if needed)
    if 'top_topic' not in df.columns:
        st.warning("No topic data found in dataset!")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    trend = df.groupby([df["publication_date"].str[:4], "top_topic"]).size().reset_index(name="count")
    sns.lineplot(data=trend, x="publication_date", y="count", hue="top_topic", marker="o", ax=ax)
    ax.set_title("Topic Hype Indicator Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Publications")
    st.pyplot(fig)