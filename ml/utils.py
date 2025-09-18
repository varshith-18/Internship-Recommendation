# ml/utils.py

def build_candidate_profile(skills="", interests="", resume_text=""):
    """
    Build a candidate profile string for embedding.
    """
    parts = [skills, interests, resume_text]
    return " ".join([p for p in parts if p])


def explain_match(candidate_skills, internship_skills):
    """
    Return overlapping skills.
    """
    cand_set = set(s.strip().lower() for s in candidate_skills.split(","))
    intern_set = set(s.strip().lower() for s in internship_skills.split(","))
    return list(cand_set.intersection(intern_set))
