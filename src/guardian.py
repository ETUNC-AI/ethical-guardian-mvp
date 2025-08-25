from transformers import pipeline
import torch
import json
import importlib.util

class EthicalGuardian:
    def __init__(self, adapter_path, config_path, prompt_path):
        self.version = "1.2-stable"

        # Load config from file
        with open(config_path, 'r') as f:
            config = json.load(f)
        model_id = config["model_id"]

        # Dynamically load prompt function from file
        spec = importlib.util.spec_from_file_location("prompts", prompt_path)
        prompts_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prompts_module)
        self.get_prompt_template = prompts_module.get_guardian_prompt

        print("Initializing model pipeline...")
        self.generator = pipeline(
            "text-generation",
            model=model_id,
            device_map="auto"
        )
        print("Pipeline initialized.")

    # This 'def' is now correctly indented to be part of the class
    def evaluate(self, test_case: dict) -> dict:
        prompt = self.get_prompt_template(test_case)
        raw_output = self.generator(
            prompt,
            max_new_tokens=350,      # Increased token limit
            do_sample=True,
            temperature=0.7          # Increased temperature for creativity
        )

        try:
            model_response_str = raw_output[0]['generated_text'].split('```json')[-1].strip()
            if model_response_str.endswith("```"):
                model_response_str = model_response_str[:-3].strip()
            parsed_json = json.loads(model_response_str)
            return parsed_json
        except Exception as e:
            return {
                "reasoning_trace": ["FATAL_PARSING_ERROR"],
                "guardian_output": f"Model failed to produce valid JSON. Error: {e}. Raw: {raw_output[0]['generated_text']}"
            }
