import json

def load_database(db_file):
    try:
        with open(db_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_to_database(db_file, data):
    with open(db_file, 'w') as file:
        json.dump(data, file, indent=4)
