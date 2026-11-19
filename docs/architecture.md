# SWE-Repair System Architecture

## Overview

SWE-Repair uses a modular architecture to separate dataset preparation, repair generation, patch validation, and isolated execution.

## Architecture

```mermaid
flowchart TB
    subgraph Dataset
        A[SWE-smith]
        B[Filtering]
        C[Metadata Enrichment]
        D[Repository Split]
        A --> B --> C --> D
    end

    subgraph Generation
        E[Task Loader]
        F[Issue Prompt Builder]
        G[Qwen Adapter]
        H[Candidate Patch]
        E --> F --> G --> H
    end

    subgraph Validation
        I[Patch Structure Check]
        J[Git Patch Check]
        H --> I --> J
    end

    subgraph Execution
        K[Docker Container]
        L[Apply Bug Injection]
        M[Apply Repair Candidate]
        N[Run Required Tests]
        K --> L --> M --> N
    end

    subgraph Results
        O[Test Outcomes]
        P[Execution Metrics]
        Q[JSON Results]
        R[Research Report]
        O --> Q
        P --> Q
        Q --> R
    end

    D --> E
    J --> K
    N --> O
    N --> P
```

## Module Responsibilities

| Module | Responsibility |
|---|---|
| Dataset preparation | Filters and organizes repair tasks |
| Task loader | Retrieves task descriptions and test information |
| Prompt builder | Formats repair instructions |
| Qwen adapter | Provides the model generation interface |
| Patch utilities | Checks candidate diff structure |
| Docker evaluator | Applies patches in isolated containers |
| Test runner | Executes required tests |
| Result processor | Stores metrics and experiment outcomes |

## Data Flow

The dataset is first filtered and divided into repository-disjoint training and testing sets.

A repair task is loaded and its issue description is converted into a structured prompt. The proposed Qwen model generates a candidate patch.

The patch is checked before being passed to the Docker evaluator. The evaluator reproduces the injected bug, applies the candidate patch, and executes the required tests.

The test outcomes and execution information are saved as structured JSON results.
