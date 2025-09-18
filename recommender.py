import pandas as pd

class InternshipRecommender:
    def __init__(self, csv_path):
        # Load dataset
        self.data = pd.read_csv(csv_path)
        # Normalize column names (lowercase + strip spaces)
        self.data.columns = [col.strip().lower() for col in self.data.columns]

    def recommend(self, user_input):
        """
        Simple recommender: filter by education, skills, sector, location
        """
        df = self.data.copy()

        # Ensure keys are lowercase
        user_input = {k.lower(): v for k, v in user_input.items() if v}

        # Filter by education
        if "education" in df.columns and user_input.get("education"):
            df = df[df["education"].str.contains(user_input["education"], case=False, na=False)]

        # Filter by skills
        if "skills" in df.columns and user_input.get("skills"):
            df = df[df["skills"].str.contains(user_input["skills"], case=False, na=False)]

        # Filter by sector
        if "sector" in df.columns and user_input.get("sectors"):
            df = df[df["sector"].str.contains(user_input["sectors"], case=False, na=False)]

        # Filter by location
        if "location" in df.columns and user_input.get("location"):
            df = df[df["location"].str.contains(user_input["location"], case=False, na=False)]

        # If no results, return empty list
        if df.empty:
            return [{"message": "No matching internships found."}]

        return df.to_dict(orient="records")
