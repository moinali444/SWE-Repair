# SWE-Repair
## AI-Based Framework for Automated Python Bug Detection and Code Repair

### 1. Project Overview
SWE-Repair is a prototype for identifying predefined Python bug patterns, applying corrections, and validating repaired code through syntax checks and automated tests.

### 2. Objectives
- Identify common Python programming errors.
- Automatically apply predefined repair rules.
- Validate repaired code using Python AST parsing.
- Evaluate repair success using test cases.
- Record evaluation results in JSON format.

### 3. Technologies Used
- Python 3.12.4
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Pytest

### 4. System Workflow
1. Input buggy Python code.
2. Detect predefined bug patterns.
3. Apply the corresponding repair rule.
4. Validate syntax.
5. Compare repaired code with expected output.
6. Store evaluation results.

### 5. Implementation
The prototype currently supports three bug patterns:
- Assignment operator instead of comparison.
- Incorrect final list index.
- Incorrect arithmetic operator.

### 6. Experimental Results
| Metric | Observed Result |
|---|---:|
| Total examples | 3 |
| Successful repairs | 3 |
| Failed repairs | 0 |
| Repair success rate | 100% |
| Pytest tests passed | 2 |

These results apply only to the predefined demonstration examples.

### 7. Limitations
- Uses predefined rule-based repairs rather than an LLM.
- Evaluated on only three demonstration examples.
- Does not yet process complete external repositories.
- Qwen2.5-Coder-3B-Instruct and LoRA fine-tuning remain planned work.

### 8. Future Enhancements
- Integrate Qwen2.5-Coder-3B-Instruct.
- Implement LoRA-based fine-tuning.
- Prepare a suitable SWE-smith task subset.
- Add repository-level context extraction.
- Expand testing to larger Python projects.

### 9. Conclusion
The prototype demonstrates a basic automated Python repair workflow, including bug-pattern detection, correction, syntax validation, and test-based evaluation. It provides an initial implementation foundation for the proposed SWE-Repair framework.