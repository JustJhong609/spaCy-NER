import os
import spacy
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="spaCy NER API")

# Cache to store loaded spacy models in memory
loaded_models = {}

class ExtractionRequest(BaseModel):
    text: str
    model: str = "en_core_web_sm"
    show_confidence: bool = True

@app.post("/extract-entities")
async def extract_entities(request: ExtractionRequest):
    model_name = request.model
    
    # 1. Retrieve or load model (caching loaded models in memory)
    if model_name not in loaded_models:
        try:
            # Attempt to load the model
            loaded_models[model_name] = spacy.load(model_name)
        except OSError:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Model '{model_name}' is not installed in the current environment. "
                    f"Please install it using: python -m spacy download {model_name}"
                )
            )
            
    nlp = loaded_models[model_name]
    
    # 2. Run Named Entity Recognition
    doc = nlp(request.text)
    
    # 3. Format & return extracted entities
    entities = []
    
    # Calculate confidence scores via Beam Search if requested
    beam_scores = {}
    if request.show_confidence:
        try:
            if "ner" in nlp.pipe_names:
                ner = nlp.get_pipe("ner")
                beams = ner.beam_parse([doc], beam_width=16, beam_density=0.0001)
                if beams:
                    for score, ents in ner.moves.get_beam_parses(beams[0]):
                        for start, end, label in ents:
                            span = doc[start:end]
                            key = (span.start_char, span.end_char, label)
                            beam_scores[key] = beam_scores.get(key, 0.0) + score
        except Exception:
            pass

    for ent in doc.ents:
        confidence = None
        if request.show_confidence:
            key = (ent.start_char, ent.end_char, ent.label_)
            confidence = round(float(beam_scores.get(key, 1.0)), 4)
        
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
            "confidence": confidence
        })
        
    return {
        "text": request.text,
        "entities": entities
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Mount the static directory to serve static assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="index.html not found in static folder.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")
    uvicorn.run("main:app", host=host, port=port, reload=True)


