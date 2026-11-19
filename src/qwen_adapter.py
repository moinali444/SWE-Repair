import json
import re
from pathlib import Path

MODEL_NAME = "Qwen/Qwen2.5-Coder-3B-Instruct"

class QwenRepairAdapter:
    """
    Qwen-based repository bug repair adapter.
    Model loading is delayed until generate() is called.
    """

    def __init__(self, model_name=MODEL_NAME, max_new_tokens=1200):
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.tokenizer = None
        self.model = None

    def build_prompt(self, task, repository_context=""):
        problem = task.get("problem_statement", "")
        repo = task.get("repo", "Unknown repository")

        tests = task.get("FAIL_TO_PASS", [])

        test_text = "\n".join("- " + str(t) for t in tests)

        return f"""
You are an expert Python software engineer specializing in
repository-level automated bug repair.

TASK
Repository: {repo}

BUG DESCRIPTION
{problem}

REQUIRED TESTS
{test_text}

REPOSITORY SOURCE CONTEXT
{repository_context}

INSTRUCTIONS
1. Identify the likely root cause.
2. Produce a minimal and correct Python code repair.
3. Do not modify unrelated functionality.
4. Preserve existing public interfaces.
5. Consider the required tests.
6. Return a unified Git diff patch only.
7. Do not invent filenames or source code.
8. Do not return explanations outside the patch.

OUTPUT FORMAT
Return a valid unified diff beginning with:

diff --git a/path/to/file b/path/to/file

Your answer must contain only the patch.
"""

    def load_model(self):
        if self.model is not None:
            return

        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
        except ImportError as exc:
            raise RuntimeError(
                "Install torch and transformers before local Qwen inference."
            ) from exc

        print("Loading model:", self.model_name)
        print("This model requires substantial RAM and storage.")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True,
            device_map="cpu",
            trust_remote_code=True
        )

        self.model.eval()
        print("Qwen model loaded successfully.")

    def extract_patch(self, response):
        text = response.strip()

        text = re.sub(r"^```(?:diff)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        start = text.find("diff --git ")

        if start < 0:
            return ""

        return text[start:].strip() + "\n"

    def generate(self, task, repository_context=""):
        self.load_model()

        prompt = self.build_prompt(task, repository_context)

        messages = [
            {
                "role": "system",
                "content": "You generate minimal valid unified Git diff patches."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        formatted = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            formatted,
            return_tensors="pt"
        )

        with __import__("torch").no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                temperature=None,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated = outputs[0][inputs["input_ids"].shape[1]:]

        response = self.tokenizer.decode(
            generated,
            skip_special_tokens=True
        )

        patch = self.extract_patch(response)

        if not patch:
            raise ValueError(
                "Qwen did not return a valid unified diff."
            )

        return patch
