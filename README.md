### **README.md**


# Interface de Recherche et Dépôt de Fichiers

Ce projet implémente une solution basée sur des **services web orientés vers les workflows**, intégrant des services d'encodage, d'insertion en base de données, de recherche, et une interface graphique utilisateur (GUI) avec Tkinter.

## **Fonctionnalités principales**
1. **Encodage des documents** :
   - Les documents textuels (ex. lois, tweets) sont encodés en vecteurs d'embedding via un modèle pré-entraîné (**SentenceTransformer**).
   - Les embeddings sont sauvegardés dans un fichier JSON.

2. **Recherche de documents** :
   - Recherche des documents similaires à une requête utilisateur en utilisant la similarité cosinus.

3. **Surveillance de fichiers (File Watcher)** :
   - Les fichiers `.txt` déposés dans le répertoire `data/input` sont automatiquement détectés, encodés et insérés dans la base.

4. **Interface graphique** :
   - Un GUI simple pour :
     - Déposer des fichiers texte dans le répertoire `input`.
     - Effectuer une recherche et afficher les résultats.



## **Arborescence du projet**

```
project_root/
├── app/
│   ├── __init__.py
│   ├── composite_service.py       # Service composite gérant l'encodage, insertion et recherche
│   ├── db_service.py              # Service gérant l'insertion en base
│   ├── embedding_service.py       # Service gérant l'encodage des documents
│   ├── utils/                     # Utilitaires (fichiers, DB, embeddings)
│       ├── __init__.py
│       ├── db_utils.py
│       ├── embedding_utils.py
│       ├── file_utils.py
├── data/
│   ├── input/                     # Répertoire de dépôt des fichiers texte
│   │   ├── donnees_melangees.txt
│   ├── output/                    # Répertoire de sortie pour le fichier database.json
│   │   ├── database.json
│   ├── lois.txt                   # Exemples de données (articles de lois)
│   ├── tweets.txt                 # Exemples de données (tweets)
├── watcher/
│   ├── file_watcher.py            # Surveille les nouveaux fichiers dans `data/input`
├── interface.py                   # Interface graphique utilisateur
├── run.ps1                        # Script PowerShell pour démarrer tous les services
├── run_services.py                # (Optionnel) Script Python pour gérer le lancement des services
├── requirements.txt               # Liste des dépendances Python
├── README.md                      # Documentation du projet
├── .env                           # Variables d'environnement (optionnel)
```

---

## **Prérequis**

- Python 3.8 ou version ultérieure
- Un environnement virtuel Python
- Les dépendances listées dans `requirements.txt`

---

## **Installation**

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Joe-azar/project_root.git
   cd project_root
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate    # Sur Linux/Mac
   venv\Scripts\activate       # Sur Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Assurez-vous que les répertoires `data/input` et `data/output` existent :
   ```bash
   mkdir -p data/input data/output
   ```

---

## **Utilisation**

### **1. Lancer les services**
Utilisez le script PowerShell pour démarrer tous les services (encodage, insertion, composite, surveillance de fichiers) et l'interface graphique :
```bash
.\run.ps1
```


### **2. Interface graphique**
L'interface graphique s'ouvre automatiquement après le lancement des services :
- **Déposer un fichier TXT** :
  - Cliquez sur le bouton pour sélectionner un fichier texte à déposer dans `data/input`.
  - Le système encode les lignes et les ajoute à la base.
- **Rechercher** :
  - Entrez une requête textuelle dans la barre de recherche et cliquez sur **Rechercher** pour afficher les résultats.

---


## **Auteurs**
- **Nom de l'auteur** : Joe Azar
- **Contact** : joe.azar@hotmail.com

---

## **Licence**
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
```
