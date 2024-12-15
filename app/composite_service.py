from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import numpy as np
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Fichier contenant les embeddings des documents
EMBEDDINGS_FILE = "./data/output/database.json"
class BatchRequest(BaseModel):
    documents: list[str]

class TextRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str

class RelevantDocument(BaseModel):
    id: int
    text: str
    similarity_score: float

class SearchResponse(BaseModel):
    relevant_documents: list[RelevantDocument]

def load_embeddings():
    try:
        with open(EMBEDDINGS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

@app.post("/batch_receive")
def batch_receive(request: BatchRequest):
    # Appeler le service d'embedding
    embedding_response = requests.post("http://localhost:8001/encode", json={"documents": request.documents})
    if embedding_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Embedding service failed")

    embeddings = embedding_response.json()

    # Appeler le service d'insertion pour tous les embeddings
    db_response = requests.post("http://localhost:8002/batch_insert", json=embeddings)
    if db_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Database service failed")

    return {"status": "success", "message": "Documents batch processed successfully"}

@app.post("/search_documents", response_model=SearchResponse)
def search_documents(request: SearchRequest):
    # Charger les embeddings
    documents = load_embeddings()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")

    # Encoder la requête utilisateur
    embedding_response = requests.post("http://localhost:8001/encode", json={"documents": [request.query]})
    if embedding_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to encode query")

    query_embedding = embedding_response.json()["embeddings"][0]["embedding"]

    # Calculer la similarité cosinus
    results = []
    for idx, doc in enumerate(documents):
        similarity = cosine_similarity(query_embedding, np.array(doc["embedding"]))
        results.append({
            "id": idx + 1,
            "text": doc["text"],
            "similarity_score": similarity
        })

    # Trier et retourner les résultats
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    return {"relevant_documents": results[:5]}
def generate_response_with_gpt(question, relevant_documents):
    """
    Utilise OpenAI GPT pour générer une réponse basée sur la question et les documents pertinents.
    """
    context = "\n\n".join([f"Document {idx + 1}: {doc['text']}" for idx, doc in enumerate(relevant_documents)])
    prompt = (
        f"Voici une question : {question}\n\n"
        f"Et voici des documents pertinents :\n\n"
        f"{context}\n\n"
        f"Répondez de manière claire et concise à la question en utilisant les informations fournies dans les documents."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,  # Limitez la réponse à une longueur raisonnable
            temperature=0.5,  # Contrôle de la créativité
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'appel à OpenAI GPT : {e}")

@app.post("/chatbot")
def chatbot(request: SearchRequest):
    """
    Répond à une question utilisateur en utilisant les documents les plus pertinents
    et OpenAI GPT pour générer une réponse.
    """
    # Charger les documents encodés
    documents = load_embeddings()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found in the database.")

    # Encoder la question utilisateur
    embedding_response = requests.post("http://localhost:8001/encode", json={"documents": [request.query]})
    if embedding_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to encode query.")

    query_embedding = embedding_response.json()["embeddings"][0]["embedding"]

    # Calculer la similarité cosinus pour chaque document
    results = []
    for doc in documents:
        similarity = cosine_similarity(query_embedding, np.array(doc["embedding"]))
        results.append({
            "text": doc["text"],
            "similarity_score": similarity
        })

    # Trier les documents par similarité
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    top_documents = results[:5]  # Prendre les 5 documents les plus pertinents

    # Générer une réponse avec OpenAI GPT
    gpt_response = generate_response_with_gpt(request.query, top_documents)

    return {
        "response": gpt_response,
        "context_documents": top_documents  # Facultatif : retournez aussi les documents pertinents
    }

# Démarrage du service en mode développement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
