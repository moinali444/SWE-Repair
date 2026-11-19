# Limitations and Future Work

## Current Limitations

1. The dataset is a pilot sample rather than the full SWE-smith benchmark.
2. The Qwen adapter interface is implemented, but actual inference has not been performed.
3. LoRA fine-tuning has not been performed.
4. Model-generated Pass@1 is unavailable.
5. The reference inverse-patch experiment is not an AI-generated repair.
6. One successfully validated task is insufficient to establish general repair capability.
7. Basic diff validation does not guarantee semantic correctness.
8. Peak model memory usage has not been measured.

## Future Work

1. Obtain compatible compute for Qwen inference.
2. Load and test the proposed base model.
3. Prepare valid supervised repair examples.
4. Implement LoRA fine-tuning.
5. Evaluate on the held-out repository-disjoint test set.
6. Compare the base model and fine-tuned model.
7. Expand the benchmark sample.
8. Report reproducible performance metrics.
