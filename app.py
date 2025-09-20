from flask import Flask, request, jsonify, render_template
from ml.recommender import InternshipRecommender
from ml.utils import explain_match

app = Flask(__name__)

# Initialize ML recommender with your CSV dataset
recommender = InternshipRecommender(csv_path="data/internships.csv")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.get_json()

    # Get top 10 recommendations from rule-based ML model
    recommendations = recommender.recommend(user_input, top_n=10)

    # Add matched_skills using utils.explain_match
    for rec in recommendations:
        rec["matched_skills"] = explain_match(
            user_input.get("skills", ""), rec.get("skills_required", "")
        )

    # Optional: print scores for debugging
    print([r["score"] for r in recommendations])

    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
