import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils.clean_mentions import clean_mentions
from collections import Counter
from typing import Dict

def calc_ai_insights(df: pd.DataFrame, company_id: str, k_top=5) -> Dict[str, Dict]:
    # Select company tweets
    company_tweets = df[df.author_id == company_id]
    # Select customer tweets addressed to the company
    customer_tweets = df[df.receiver == company_id]
    tweets = df.text.dropna().tolist()
    # Clean any mention
    tweets = [clean_mentions(tweet) for tweet in tweets]
    # Load an encoder model to generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(tweets)

    # Search for clusters within the tweets given the encoder embeddings
    num_topics = min(k_top, len(tweets))
    kmeans = KMeans(n_clusters=num_topics, random_state=42)
    kmeans.fit(embeddings)
    labels = kmeans.labels_

    # Top keywords on each cluster
    top_keywords = get_top_keywords(tweets, labels, n_keywords=5)
    cluster_counts = dict(Counter(kmeans.labels_))

    # Arange top issues output
    top_issues = {}
    for label, keywords in top_keywords.items():
        top_issues[label.item()] = " ".join(keywords)
    # Arange top counts output
    top_counts = {}
    for label, count in cluster_counts.items():
        top_counts[label.item()] = count

    return {"top_issues": top_issues, "top_counts": top_counts}

def get_top_keywords(tweets, labels, n_keywords=5):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(tweets[i])

    cluster_keywords = {}
    for label, cluster_tweets in clusters.items():
        tfidf_matrix = vectorizer.fit_transform(cluster_tweets)
        feature_names = vectorizer.get_feature_names_out()
        dense = tfidf_matrix.todense()
        summed = dense.sum(axis=0).A1
        word_scores = zip(feature_names, summed)
        sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, score in sorted_words[:n_keywords]]
        cluster_keywords[label] = top_keywords

    return cluster_keywords