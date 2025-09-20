# ml/utils.py
import re

def build_candidate_profile(skills="", sectors="", location="", education="", resume_text=""):
    """
    Build a candidate profile string for embedding or scoring.
    Combines skills, sector interests, location, education, and optional resume text.
    """
    parts = [education, skills, sectors, location, resume_text]
    return " ".join([p for p in parts if p])


def parse_skills(skill_text):
    """
    Parse a skills string into a set of normalized skills.
    Handles comma, semicolon, or whitespace separation.
    """
    skills = re.split(r"[;,\\s]+", skill_text.lower())
    return {s.strip() for s in skills if s.strip()}


def explain_match(candidate_skills, internship_skills):
    """
    Return overlapping skills between candidate and internship.
    Accepts strings (comma/semicolon separated) or sets.
    """
    # Convert strings to sets if necessary
    if isinstance(candidate_skills, str):
        candidate_skills = parse_skills(candidate_skills)
    if isinstance(internship_skills, str):
        internship_skills = parse_skills(internship_skills)

    return list(candidate_skills.intersection(internship_skills))
