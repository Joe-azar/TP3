import os
import shutil
import requests
import tkinter as tk
from tkinter import filedialog, messagebox

# Chemins vers les répertoires
INPUT_DIR = "./data/input/"
SEARCH_API_URL = "http://localhost:8000/search_documents"
CHATBOT_API_URL = "http://localhost:8000/chatbot"

# Fonction pour déposer un fichier dans le répertoire `input`
def deposit_file():
    file_path = filedialog.askopenfilename(
        title="Sélectionner un fichier TXT",
        filetypes=[("Fichiers TXT", "*.txt")]
    )
    if file_path:
        try:
            shutil.copy(file_path, INPUT_DIR)
            messagebox.showinfo("Succès", "Fichier déposé avec succès dans le répertoire input!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la copie du fichier : {e}")

# Fonction pour effectuer une recherche
def perform_search():
    query = search_entry.get()
    if not query.strip():
        messagebox.showerror("Erreur", "Veuillez entrer une requête de recherche.")
        return

    try:
        response = requests.post(SEARCH_API_URL, json={"query": query})
        if response.status_code == 200:
            results = response.json()["relevant_documents"]
            results_text.delete(1.0, tk.END)
            for doc in results:
                results_text.insert(tk.END, f"ID: {doc['id']}\n")
                results_text.insert(tk.END, f"Texte: {doc['text']}\n")
                results_text.insert(tk.END, f"Score: {doc['similarity_score']:.2f}\n")
                results_text.insert(tk.END, "-"*40 + "\n")
        else:
            messagebox.showerror("Erreur", f"Erreur API : {response.json()['detail']}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

def ask_chatbot():
    query = chatbot_entry.get()
    if not query.strip():
        messagebox.showerror("Erreur", "Veuillez entrer une question.")
        return

    try:
        response = requests.post("http://localhost:8000/chatbot", json={"query": query})
        if response.status_code == 200:
            answer = response.json()["response"]
            chatbot_response_text.delete(1.0, tk.END)
            chatbot_response_text.insert(tk.END, f"Question : {query}\nRéponse : {answer}")
        else:
            messagebox.showerror("Erreur", f"Erreur API : {response.json()['detail']}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la communication avec le chatbot : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface Recherche et Dépôt de Fichiers")

# Bouton pour déposer un fichier
deposit_button = tk.Button(root, text="Déposer un fichier TXT", command=deposit_file, width=30)
deposit_button.pack(pady=10)

# Barre de recherche
search_label = tk.Label(root, text="Rechercher :")
search_label.pack(pady=5)
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

# Bouton de recherche
search_button = tk.Button(root, text="Rechercher", command=perform_search, width=20)
search_button.pack(pady=10)

# Zone pour afficher les résultats
results_text = tk.Text(root, height=20, width=80)
results_text.pack(pady=10)
# Interface Tkinter
root = tk.Tk()
root.title("Chatbot")
# Section chatbot
chatbot_label = tk.Label(root, text="Posez une question au Chatbot :")
chatbot_label.pack(pady=5)
chatbot_entry = tk.Entry(root, width=50)
chatbot_entry.pack(pady=5)
chatbot_button = tk.Button(root, text="Envoyer", command=ask_chatbot, width=20)
chatbot_button.pack(pady=10)
chatbot_response_text = tk.Text(root, height=10, width=80)
chatbot_response_text.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
