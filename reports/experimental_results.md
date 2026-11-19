# SWE-Repair — Experimental Results and Project Audit

Generated: 2026-11-19T18:50:02.395848+00:00

## 1. Dataset

- Training records: 118
- Testing records: 35
- Total records: 153
- Training repositories: 21
- Testing repositories: 6
- Repository overlap: 0
- Repository-disjoint split: True

## 2. Patch format validation

### train_full.jsonl
- Total: 118
- Basic diff structure valid: 118
- Invalid: 0

### test_full.jsonl
- Total: 35
- Basic diff structure valid: 35
- Invalid: 0

## 3. Docker benchmark validation

- Task: Not recorded
- Clean baseline: {'passed': 2, 'failed': 0, 'status': 'PASS'}
- Bug-patched execution: {'passed': 0, 'failed': 2, 'status': 'FAIL', 'failure_summary': ['Version._get_canonical() returned .post0 instead of 1.0', 'parse_version() rejected the generated .post0 version']}
- Interpretation: The injected bug reproduced the expected test failures.

## 4. Repair experiments

### repair_eval_facelessuser__soupsieve.a8080d97.combine_file__c4wdlqg7.json
- Task: facelessuser__soupsieve.a8080d97.combine_file__c4wdlqg7
- Status: passed
- Candidate type: unspecified
- Tests passed: None
- Tests failed: None
- Model generated: False
- Model Pass@1: None
- Interpretation: 

## 5. AI model status

- Qwen adapter implementation: created and unit-tested.
- Actual Qwen inference: not completed.
- LoRA fine-tuning: not completed.
- AI-generated benchmark Pass@1: not available.

## 6. Required project files

- [x] `main.py`
- [x] `README.md`
- [x] `evaluate_repair.py`
- [x] `generate_repair.py`
- [x] `src/repair_agent.py`
- [x] `src/repair_pipeline.py`
- [x] `src/qwen_adapter.py`
- [x] `src/patch_utils.py`
- [x] `data/train_full.jsonl`
- [x] `data/test_full.jsonl`
- [x] `results/benchmark_validation.json`

## 7. Limitations

The current validated repair experiment uses an oracle inverse of the SWE-smith injected bug patch. It demonstrates that the Docker-based evaluation pipeline can reproduce failures and verify a repair. It is not a Qwen-generated result.

The Qwen adapter is an implementation interface. Model weights have not been loaded, inference has not been completed, and LoRA training has not been performed.

Patch-format checks verify basic unified-diff structure only. They do not establish semantic correctness.

## 8. Conclusion

The project has a prepared SWE-smith dataset, repository-based train/test separation, patch validation, Docker-based bug reproduction, an automated repair evaluator, an oracle repair validation experiment, and a tested Qwen adapter interface.
Actual AI-model training and benchmark evaluation remain future work.
