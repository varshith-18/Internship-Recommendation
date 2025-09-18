from flask import Flask, render_template, request, jsonify
from recommender import InternshipRecommender

app = Flask(__name__)
recommender = InternshipRecommender("data/internships.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    # Pass user input safely
    recommendations = recommender.recommend({
        "education": data.get("education", ""),
        "skills": data.get("skills", ""),
        "sectors": data.get("sectors", ""),
        "location": data.get("location", "")
    })

    return jsonify(recommendations)

if __name__ == "__main__":
    print(">>> Flask app starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)
