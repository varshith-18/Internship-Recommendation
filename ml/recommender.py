# ml/recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer, util
    USE_BERT = True
except ImportError:
    USE_BERT = False
    print("⚠️ sentence-transformers not installed. Falling back to TF-IDF.")


class InternshipRecommender:
    def __init__(self, csv_path: str):
        # Load dataset
        self.df = pd.read_csv(csv_path)
        self.df.fillna("", inplace=True)

        # Combine relevant fields for semantic search
        self.df["combined"] = (
            self.df["title"].astype(str) + " " +
            self.df["sector"].astype(str) + " " +
            self.df["skills_required"].astype(str) + " " +
            self.df["location"].astype(str) + " " +
            self.df["description"].astype(str)
        )

        if USE_BERT:
            print("✅ Using Sentence-BERT for embeddings...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.embeddings = self.model.encode(
                self.df["combined"].tolist(),
                convert_to_tensor=True,
                show_progress_bar=True
            )
        else:
            print("✅ Using TF-IDF for similarity...")
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined"])

    def recommend(self, user_input: dict, top_n: int = 5):
        # Combine user preferences into one query string
        query = " ".join([
            user_input.get("education", ""),
            user_input.get("skills", ""),
            user_input.get("sectors", ""),
            user_input.get("location", "")
        ])

        if USE_BERT:
            query_vec = self.model.encode(query, convert_to_tensor=True)
            scores = util.cos_sim(query_vec, self.embeddings)[0].cpu().tolist()
        else:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Rank internships
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]

        recommendations = []
        for idx in top_indices:
            row = self.df.iloc[idx]
            recommendations.append({
                "id": int(row.get("id", -1)),
                "title": row.get("title", "Unknown"),
                "sector": row.get("sector", "Unknown"),
                "location": row.get("location", "Unknown"),
                "skills_required": row.get("skills_required", "Not specified"),
                "description": row.get("description", ""),
                "score": round(float(scores[idx]), 2)
            })

        return recommendations
