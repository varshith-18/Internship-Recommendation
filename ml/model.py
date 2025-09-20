# ml/model.py
import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class InternshipRecommender:
    def __init__(self, data_path="data/internships.csv"):
        """
        Load internship dataset and prepare embeddings (for optional tiebreak).
        """
        self.internships = pd.read_csv(data_path)
        self.internships.fillna("", inplace=True)

        # Sentence-BERT for optional semantic similarity
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Precompute embeddings for descriptions
        self.internships["doc"] = (
            self.internships["title"].astype(str) + " " +
            self.internships["description"].astype(str) + " " +
            self.internships["required_skills"].astype(str)
        )
        self.embeddings = self.model.encode(
            self.internships["doc"].tolist(), convert_to_numpy=True
        )

    def _parse_skills(self, text: str):
        """Split skills by comma/semicolon/space, lowercase, strip."""
        skills = re.split(r"[;,\s]+", str(text).lower())
        return {s.strip() for s in skills if s.strip()}

    def recommend(self, candidate: dict, topk: int = 10):
        """
        Rule-based recommendation with optional semantic tiebreak.
        candidate = {
            "education": "...",
            "skills": "python, ml, teamwork",
            "sectors": "data science",
            "location": "pune"
        }
        """
        user_skills = self._parse_skills(candidate.get("skills", ""))
        user_sector = candidate.get("sectors", "").lower()
        user_location = candidate.get("location", "").lower()

        # Build candidate string for BERT tiebreak
        cand_text = " ".join([
            candidate.get("education", ""),
            candidate.get("skills", ""),
            candidate.get("sectors", ""),
            candidate.get("location", "")
        ])
        cand_emb = self.model.encode([cand_text], convert_to_numpy=True)
        semantic_sims = cosine_similarity(cand_emb, self.embeddings)[0]

        scores = []
        for idx, row in self.internships.iterrows():
            intern_skills = self._parse_skills(row["required_skills"])
            skill_overlap = len(user_skills.intersection(intern_skills)) / max(1, len(intern_skills))

            if skill_overlap == 0:
                scores.append(0)
                continue

            sector_boost = 0.1 if user_sector and user_sector in row["description"].lower() else 0
            location_boost = 0.1 if user_location and user_location in row["location"].lower() else 0

            # Rule-based dominates, semantic is only small boost
            final_score = skill_overlap + sector_boost + location_boost + 0.05 * semantic_sims[idx]
            scores.append(final_score)

        self.internships["score"] = scores
        ranked = self.internships.sort_values("score", ascending=False)

        # Also return match % for UI
        max_score = max(scores) or 1
        ranked["match_percent"] = (ranked["score"] / max_score * 100).round().astype(int)

        return ranked.head(topk)[
            ["title", "company", "location", "required_skills", "score", "match_percent"]
        ]
