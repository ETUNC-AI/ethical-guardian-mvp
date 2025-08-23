import json

def load_corpus(file_path):
    """
    Loads a JSON corpus from the given file path.
    """
    print(f"Attempting to load corpus from {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print("Corpus loaded successfully.")
        return data
    except FileNotFoundError:
        print("ERROR: Corpus file not found.")
        return None
    except json.JSONDecodeError:
        print("ERROR: Corpus file is not valid JSON.")
        return None
