from flask import Flask, render_template, request, jsonify
from ml.recommender import InternshipRecommender

app = Flask(__name__)

# Load your recommender
recommender = InternshipRecommender("data/internships.csv")

# Route for homepage (index.html)
@app.route("/")
def home():
    return render_template("index.html")   # <-- loads your index.html

# Route to handle recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = {
        "education": request.form.get("education", ""),
        "skills": request.form.get("skills", ""),
        "sectors": request.form.get("sectors", ""),
        "location": request.form.get("location", "")
    }
    results = recommender.recommend(user_input, top_n=5)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
