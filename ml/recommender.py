# ml/recommender.py
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Default to False
USE_BERT = False

# Try to import Sentence-BERT
try:
    from sentence_transformers import SentenceTransformer, util
    USE_BERT = True
except ImportError:
    USE_BERT = False
    # Dummy util to avoid Pylance warnings
    class DummyUtil:
        @staticmethod
        def cos_sim(a, b):
            return 0
    util = DummyUtil()
    print("⚠️ sentence-transformers not installed. Falling back to TF-IDF.")


class InternshipRecommender:
    def __init__(self, csv_path: str):
        # Load dataset
        self.df = pd.read_csv(csv_path)
        self.df.fillna("", inplace=True)

        # Combine fields for semantic search
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

    def _parse_skills(self, text: str):
        """Split skills by comma or semicolon, lowercase, strip spaces."""
        skills = re.split(r"[;,]", str(text).lower())
        return {s.strip() for s in skills if s.strip()}

    def recommend(self, user_input: dict, top_n: int = 5, unique: bool = True):
        # Combine user preferences into a query string
        query = " ".join([
            user_input.get("education", ""),
            user_input.get("skills", ""),
            user_input.get("sectors", ""),
            user_input.get("location", "")
        ])

        # Compute similarity scores (optional, minor weight)
        if USE_BERT:
            query_vec = self.model.encode(query, convert_to_tensor=True)
            scores = util.cos_sim(query_vec, self.embeddings)[0].cpu().tolist()
        else:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Prepare user skills, sector, location
        user_skills = self._parse_skills(user_input.get("skills", ""))
        user_sector = user_input.get("sectors", "").lower()
        user_location = user_input.get("location", "").lower()

        boosted_scores = []
        for idx, row in self.df.iterrows():
            intern_skills = self._parse_skills(row["skills_required"])
            skill_overlap = len(user_skills.intersection(intern_skills)) / max(1, len(intern_skills))

            # Skip internships with no skill match
            if skill_overlap == 0:
                boosted_scores.append(0)
                continue

            # Sector/location boosts with substring matching
            sector_boost = 0.1 if user_sector and user_sector in row["sector"].lower() else 0
            location_boost = 0.1 if user_location and user_location in row["location"].lower() else 0

            # Final score: skill overlap dominates, similarity minor tiebreaker
            final_score = skill_overlap + sector_boost + location_boost + 0.05 * scores[idx]
            boosted_scores.append(final_score)

        # Normalize scores to 0-1
        max_score = max(boosted_scores) or 1
        boosted_scores = [s / max_score for s in boosted_scores]

        # Rank by boosted scores
        top_indices = sorted(range(len(boosted_scores)), key=lambda i: boosted_scores[i], reverse=True)

        # Prepare recommendation output
        recommendations = []
        seen_titles = set()
        for idx in top_indices:
            if len(recommendations) >= top_n:
                break

            row = self.df.iloc[idx]
            key = (row.get("title", ""), row.get("location", ""))
            if unique and key in seen_titles:
                continue
            seen_titles.add(key)

            intern_skills = self._parse_skills(row["skills_required"])
            matched_skills = list(user_skills.intersection(intern_skills))

            score_val = float(boosted_scores[idx])

            recommendations.append({
                "id": int(row.get("id", -1)),
                "title": row.get("title", "Unknown"),
                "sector": row.get("sector", "Unknown"),
                "location": row.get("location", "Unknown"),
                "skills_required": row.get("skills_required", "Not specified"),
                "description": row.get("description", ""),
                "score": round(score_val, 2),
                "match_percent": int(round(score_val * 100)),
                "matched_skills": matched_skills
            })

        return recommendations
