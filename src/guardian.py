from transformers import pipeline
import torch
import json
import importlib.util

class EthicalGuardian:
    def __init__(self, adapter_path, config_path, prompt_path):
        self.version = "1.6-gpu-final"

        with open(config_path, 'r') as f:
            config = json.load(f)
        model_id = config["model_id"]

        spec = importlib.util.spec_from_file_location("prompts", prompt_path)
        prompts_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prompts_module)
        self.get_prompt_template = prompts_module.get_guardian_prompt

        print("Initializing model pipeline for GPU...")
        self.generator = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.float16, # Use float16 for better GPU performance
            device=0 # Explicitly assign to the first GPU
        )
        print("Pipeline initialized.")

    def evaluate(self, test_case: dict) -> dict:
        prompt = self.get_prompt_template(test_case)
        raw_output = self.generator(
            prompt,
            max_new_tokens=350,
            do_sample=True,
            temperature=0.7
        )

        try:
            raw_text = raw_output[0]['generated_text']
            # Find the first JSON block, delineated by ```json and ```
            json_block_start = raw_text.find('```json')
            if json_block_start != -1:
                # Adjust start index to be after ```json
                start_index = json_block_start + len('```json')
                end_index = raw_text.find('```', start_index)
                if end_index != -1:
                    json_str = raw_text[start_index:end_index].strip()
                    # Replace single quotes just in case
                    json_str = json_str.replace("'", '"')
                    parsed_json = json.loads(json_str)
                    return parsed_json

            # Fallback for models that don't use markdown
            start_index = raw_text.find('{')
            end_index = raw_text.rfind('}') + 1
            if start_index != -1 and end_index != 0:
                json_str = raw_text[start_index:end_index]
                json_str = json_str.replace("'", '"')
                parsed_json = json.loads(json_str)
                return parsed_json

            raise ValueError("No valid JSON object found in the model's output.")

        except Exception as e:
            return {
                "reasoning_trace": ["FATAL_PARSING_ERROR"],
                "guardian_output": f"Model failed to produce valid JSON. Error: {e}. Raw: {raw_output[0]['generated_text']}"
            }
