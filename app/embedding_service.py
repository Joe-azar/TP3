from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

class EmbeddingRequest(BaseModel):
    documents: list[str]

@app.post("/encode")
def encode_documents(request: EmbeddingRequest):
    try:
        embeddings = [{"text": doc, "embedding": model.encode(doc).tolist()} for doc in request.documents]
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'encodage : {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
