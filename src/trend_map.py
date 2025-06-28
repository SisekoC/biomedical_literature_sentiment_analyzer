import plotly.express as px
import streamlit as st
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_interactive_trend_map(df):
    # Vectorize abstracts
    vectorizer = TfidfVectorizer(max_features=500)
    vectors = vectorizer.fit_transform(df["abstract"].fillna("")).toarray()

    # t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, perplexity=30, max_iter=1000, random_state=42)
    tsne_result = tsne.fit_transform(vectors)

    df["tsne_x"] = tsne_result[:, 0]
    df["tsne_y"] = tsne_result[:, 1]

    fig = px.scatter(
        df,
        x="tsne_x",
        y="tsne_y",
        hover_data=["title", "journal", "publication_date"],
        color="sentiment_score",
        color_continuous_scale="RdBu",
        title="Interactive Trend Map (t-SNE)"
    )

    st.plotly_chart(fig, use_container_width=True)
