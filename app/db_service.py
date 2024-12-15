from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()
DB_FILE = "./data/output/database.json"

class BatchInsertRequest(BaseModel):
    embeddings: list[dict]

@app.post("/batch_insert")
def batch_insert(request: BatchInsertRequest):
    try:
        # Charger la base de données existante
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        # Ajouter les nouveaux embeddings
        data.extend(request.embeddings)

        # Sauvegarder les modifications dans le fichier
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)

        return {"status": "success", "message": f"{len(request.embeddings)} documents insérés avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'insertion : {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
