# ml/model.py
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class InternshipRecommender:
    def __init__(self, data_path="data/internships.csv"):
        """
        Load internship dataset and prepare embeddings.
        """
        self.internships = pd.read_csv(data_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Create a combined text column
        self.internships["doc"] = (
            self.internships["title"].fillna("") + " " +
            self.internships["description"].fillna("") + " " +
            self.internships["required_skills"].fillna("")
        )

        # Precompute internship embeddings
        self.embeddings = self.model.encode(
            self.internships["doc"].tolist(), convert_to_numpy=True
        )

    def recommend(self, candidate_text: str, topk: int = 10):
        """
        Recommend internships for a candidate profile string.
        """
        cand_emb = self.model.encode([candidate_text], convert_to_numpy=True)
        sims = cosine_similarity(cand_emb, self.embeddings)[0]

        self.internships["score"] = sims
        ranked = self.internships.sort_values("score", ascending=False)

        return ranked.head(topk)[["title", "company", "location", "score"]]
