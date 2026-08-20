from functools import lru_cache

import spacy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="spaCy NER API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EntityRequest(BaseModel):
    text: str
    model: str = "en_core_web_sm"


@lru_cache(maxsize=8)
def get_model(model_name: str):
    try:
        return spacy.load(model_name)
    except OSError as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                f"spaCy model '{model_name}' is not installed. "
                f"Install it with: python -m spacy download {model_name}"
            ),
        ) from exc


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract-entities")
def extract_entities(payload: EntityRequest):
    if not payload.text.strip():
        return {"text": payload.text, "entities": []}

    doc = get_model(payload.model)(payload.text)
    entities = [
        {
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
        }
        for ent in doc.ents
    ]
    return {"text": payload.text, "entities": entities}
