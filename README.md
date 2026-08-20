# spaCy-NER

Simple local NER testing app using FastAPI + spaCy + a single HTML frontend.

## 1) Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Optional models for the dropdown:

```bash
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg
```

## 2) Run backend API

```bash
uvicorn app:app --reload
```

Backend endpoints:
- `GET /health`
- `POST /extract-entities`

Example request body:

```json
{
  "text": "Apple was founded by Steve Jobs in California.",
  "model": "en_core_web_sm"
}
```

## 3) Open frontend

Open `/home/runner/work/spaCy-NER/spaCy-NER/index.html` in a browser.

Then:
1. Enter text
2. Pick model
3. Click **Extract Entities**