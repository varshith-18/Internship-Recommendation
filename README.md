# SIH PM Internship Recommender — Prototype

## Setup (Linux / macOS)
1. Create a venv: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `python app.py` (or `flask run` after exporting FLASK_APP)
5. Open `http://127.0.0.1:5000/` in your browser.

## Setup (Windows PowerShell)
1. `python -m venv venv`
2. `venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. `python app.py`
5. `pip install scikit-learn`
6. `pip install sentence-transformers`

## Test quickly (curl)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"education":"Bachelors","skills":"python,pandas","sectors":"Data Science","location":"New Delhi"}' http://127.0.0.1:5000/recommend
