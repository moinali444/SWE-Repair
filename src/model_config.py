
MODEL_NAME = "Qwen/Qwen2.5-Coder-3B-Instruct"

MODEL_SETTINGS = {
    "model_name": MODEL_NAME,
    "task": "text-generation",
    "max_new_tokens": 1024,
    "temperature": 0.1,
    "do_sample": False
}

LORA_SETTINGS = {
    "r": 8,
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "target_modules": [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj"
    ],
    "task_type": "CAUSAL_LM"
}

if __name__ == "__main__":
    print("========== SWE-REPAIR MODEL CONFIGURATION ==========")
    print("Base model:", MODEL_NAME)
    print("\nModel settings:")
    for key, value in MODEL_SETTINGS.items():
        print(f"{key}: {value}")

    print("\nLoRA settings:")
    for key, value in LORA_SETTINGS.items():
        print(f"{key}: {value}")
