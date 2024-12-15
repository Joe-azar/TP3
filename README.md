Voici le **README.md** mis à jour pour refléter que votre application est lancée avec **`.\run.ps1`** :

---

### **README.md**

```markdown
# Chatbot et Recherche avec FastAPI et Tkinter

Ce projet est une application combinant un chatbot basé sur OpenAI GPT et un moteur de recherche de documents, le tout intégré dans une interface graphique (Tkinter).

## **Fonctionnalités**
1. **Dépôt de fichiers** :
   - Déposez des fichiers texte dans le répertoire `data/input/` via l'interface graphique.
   - Les fichiers sont surveillés et automatiquement encodés.

2. **Recherche de documents** :
   - Recherchez des documents pertinents en fonction d'une requête utilisateur.
   - Affiche les documents avec un score de similarité > 0.2.

3. **Chatbot intelligent** :
   - Posez une question au chatbot et recevez une réponse générée à partir des documents encodés.

## **Installation**
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/mon-projet.git
   cd mon-projet
   ```

2. Créez un environnement virtuel et installez les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate       # Sur Linux/MacOS
   venv\Scripts\activate          # Sur Windows
   pip install -r requirements.txt
   ```

3. Configurez votre clé OpenAI API dans le fichier `.env` :
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## **Lancer l'application**
1. Utilisez le script PowerShell **`run.ps1`** pour démarrer tous les services ainsi que l'interface graphique :
   ```bash
   .\run.ps1
   ```

2. Une fois le script exécuté :
   - **Services** :
     - FastAPI sera disponible à : [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Interface graphique** :
     - Une fenêtre Tkinter s'ouvrira automatiquement pour interagir avec l'application.

---

## **Utilisation**
- **Déposer un fichier** : Cliquez sur le bouton **Déposer un fichier TXT** pour ajouter des documents à encoder.
- **Rechercher des documents** : Entrez une requête dans la barre de recherche et cliquez sur **Rechercher**.
- **Poser une question au chatbot** : Posez une question dans le champ du chatbot et cliquez sur **Envoyer**.

---

## **Auteurs**
- **Nom de l'auteur** : Joe Azar
- **Contact** : joe.azar@hotmail.com

---

## **Licence**
Ce projet est sous licence MIT.
```
