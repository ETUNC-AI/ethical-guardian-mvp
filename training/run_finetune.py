import json
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer
import torch

def run_finetuning():
    """
    Main function to execute the LoRA fine-tuning process.
    """
    print("--- Starting Fine-Tuning Process for Guardian v2.0 ---")

    # Load config and model ID
    with open('config.json', 'r') as f:
        config = json.load(f)
    model_id = config["model_id"]

    print(f"Loading base model: {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    # Add a padding token if one doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map="auto",
        torch_dtype=torch.float16 # Use float16 for GPU performance
    )

    # Load the formatted dataset
    print("Loading formatted dataset...")
    dataset = load_dataset("json", data_files="data_processing/finetuning_data_v2.jsonl", split="train")

    # Configure LoRA
    lora_config = LoraConfig(
        r=8,
        target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    print("LoRA adapters injected into model.")

    # Set training arguments
    training_args = TrainingArguments(
        output_dir="./models/guardian_v2_adapter",
        num_train_epochs=3,
        per_device_train_batch_size=1, # Use a smaller batch size for the larger model
        gradient_accumulation_steps=4, # Accumulate gradients to simulate a larger batch size
        logging_steps=5,
        save_steps=50,
    )

    # Initialize Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        args=training_args,
        max_seq_length=2048, # Increase sequence length for more detailed responses
        dataset_text_field="text",
        tokenizer=tokenizer,
    )

    print("--- Beginning Training Run ---")
    trainer.train()
    print("--- Training Run Complete ---")

    # Save the trained adapter
    print("Saving LoRA adapter for Guardian v2.0...")
    model.save_pretrained("./models/guardian_v2_adapter")
    print("Adapter saved successfully.")

if __name__ == "__main__":
    run_finetuning()
