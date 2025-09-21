from ml.recommender import InternshipRecommender

# Use the correct CSV path
recommender = InternshipRecommender("data/internships.csv")

# Example user input
user_input = {
    "education": "B.Tech Computer Science",
    "skills": "Python, Machine Learning",
    "sectors": "Data Science",
    "location": "New Delhi"
}

# Get top 5 recommendations
results = recommender.recommend(user_input, top_n=5)

# Print nicely
for i, rec in enumerate(results, 1):
    print(f"{i}. {rec['title']} ({rec['sector']}) at {rec['location']}")
    print(f"   Skills Required: {rec['skills_required']}")
    print(f"   Score: {rec['score']}")
    print(f"   Description: {rec['description'][:100]}...\n")
