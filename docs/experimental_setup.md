# SWE-Repair Experimental Setup

## Hardware

Development system:
- GPU: NVIDIA GeForce RTX 3050 Laptop GPU, 6 GB VRAM.
- System memory: 16 GB RAM.
- Operating system: Windows 11.
- CPU-side development: Python 3.12.4.

GPU availability through the installed PyTorch environment was not confirmed.

## Software

- Python 3.12.4.
- Docker Desktop.
- WSL2 with Ubuntu.
- pytest.
- Git.
- JSONL-based dataset storage.

## Dataset

- Dataset: SWE-smith.
- Prepared usable sample: 153 tasks.
- Training split: 118 tasks.
- Testing split: 35 tasks.
- Repository overlap: zero.

## Docker Validation

Selected task:

facelessuser__soupsieve.a8080d97.combine_file__c4wdlqg7

The clean baseline passed both required tests.

After applying the dataset bug-injection patch, both required tests failed.

After applying the oracle inverse patch, both required tests passed.

## Interpretation

This experiment validates the selected Docker test workflow.

It does not represent a Qwen-generated repair or a model Pass@1 result.

## Model Experiment Status

- Qwen adapter source: implemented.
- Adapter unit tests: passed.
- Actual model loading: not completed.
- Actual inference: not completed.
- LoRA training: not completed.
- Model benchmark: not completed.
