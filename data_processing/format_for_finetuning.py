import json
import sys
import os

# Add the project root to the Python path to allow importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.corpus_loader import load_corpus

def format_data(input_path: str, output_path: str):
    """
    Loads a raw corpus, formats it for instruction fine-tuning,
    and saves it as a JSON Lines file.
    """
    print(f"Loading raw corpus from {input_path}...")
    raw_corpus = load_corpus(input_path)
    if not raw_corpus:
        print("Formatting failed.")
        return

    print(f"Formatting data and saving to {output_path}...")
    with open(output_path, 'w') as f:
        for entry in raw_corpus:
            # Ensure the ideal_response is a JSON string
            ideal_response_json = json.dumps(entry.get("ideal_response"))

            # This is the structured text format the model will be trained on
            formatted_text = f"<start_of_turn>user\n{entry.get('prompt')}<end_of_turn>\n<start_of_turn>model\n{ideal_response_json}<end_of_turn>"

            # Each line in the output file is a separate JSON object
            json_line = json.dumps({"text": formatted_text})
            f.write(json_line + '\n')

    print("Formatting complete.")

if __name__ == '__main__':
    # Use the new Canadian-aligned corpus as the input
    INPUT_FILE = 'phase_b_corpus_v2_canadian_aligned.json'
    OUTPUT_FILE = 'data_processing/finetuning_data_v2.jsonl'
    format_data(INPUT_FILE, OUTPUT_FILE)
