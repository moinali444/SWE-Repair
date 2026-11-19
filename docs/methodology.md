# SWE-Repair Research Methodology

## 1. Research Design

This project follows an experimental approach to repository-level automated program repair.

The objective is to investigate whether a code-generation model can generate patches that resolve Python software defects while preserving existing functionality.

## 2. Dataset

The SWE-smith dataset is used to construct repair tasks.

The prepared pilot contains 153 usable examples:

- Training: 118 examples.
- Testing: 35 examples.
- Training repositories: 21.
- Testing repositories: 6.

A repository-grouped split is used to reduce repository leakage between training and evaluation.

## 3. Data Preparation

The preparation process includes:

1. Dataset sampling.
2. Removal of unusable records.
3. Deduplication.
4. Metadata recovery.
5. Repository-based train/test separation.
6. Unified diff format validation.

## 4. Proposed Model

Qwen2.5-Coder-3B-Instruct is the proposed code-generation model.

LoRA is the proposed parameter-efficient fine-tuning approach.

The model is expected to receive issue descriptions and relevant repository context and produce unified diff patches.

## 5. Repair Generation

The repair generation stage uses a structured prompt containing:

- Repository identification.
- Bug description.
- Required tests.
- Relevant source context.
- Instructions for producing a minimal patch.

The generated output is expected to be a unified Git diff.

## 6. Patch Validation

Candidate patches undergo structural validation before execution.

Validation includes:

- Checking for an empty patch.
- Checking for a Git diff header.
- Checking for unified diff hunks.
- Checking patch applicability in the target repository.

## 7. Isolated Evaluation

Docker is used to isolate repository-level repair experiments.

The evaluation process:

1. Starts the task environment.
2. Applies the injected bug patch.
3. Applies the candidate repair.
4. Executes the required failing tests.
5. Records test outcomes and execution time.

## 8. Evaluation Metrics

The planned metrics are:

- Pass@1.
- Repair success rate.
- Test pass rate.
- Execution time.
- Peak memory usage.

These metrics will be reported for actual model-generated repairs only after model evaluation.

## 9. Reproducibility

The project stores task information, patch files, experiment outcomes, and metadata in structured files.

Docker provides a reproducible execution environment for the selected task.

## 10. Current Scope

The current implementation validates the data and evaluation infrastructure. The proposed Qwen inference and LoRA training stages remain future experimental work.
