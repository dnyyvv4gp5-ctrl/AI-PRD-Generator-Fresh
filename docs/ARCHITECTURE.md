# AI PRD Generator
# Technical Architecture Document

## 1. Architecture Overview

The application will use a modular architecture built with
Python and Streamlit.

The architecture separates the user interface, application
workflow, AI generation, output validation and evaluation.

## 2. Architecture Components

### 2.1 User Interface
Technology: Streamlit

Responsibilities:
- Collect product ideas and supporting context.
- Display the guided generation workflow.
- Present generated PRD sections.
- Allow users to review and edit content.
- Support light and dark themes.
- Provide document export.

### 2.2 Application Workflow
Technology: Python

Responsibilities:
- Manage the generation workflow.
- Validate user inputs.
- Coordinate AI generation.
- Manage errors and application states.
- Connect the interface with backend modules.

### 2.3 AI Generation Engine
Technology: Generative AI / LLM

Responsibilities:
- Analyse product ideas.
- Generate problem statements.
- Generate user stories.
- Generate acceptance criteria.
- Suggest success metrics.
- Assemble structured PRD content.

AI generation must follow defined prompts and output
requirements.

### 2.4 Output Validation
Technology: Pydantic

Responsibilities:
- Validate generated output structure.
- Check required fields.
- Identify missing sections.
- Validate data types and expected formats.
- Reject malformed outputs.

### 2.5 Evaluation Engine
Technology: Python (rule-based heuristic evaluation)

Responsibilities:
- Evaluate generated output quality.
- Record test results.
- Assess relevance, completeness and consistency.
- Analyse unsupported assumptions.
- Compare results across test cases.

### 2.6 Testing
Technology: Pytest

Responsibilities:
- Test individual application modules.
- Validate output schemas.
- Test error handling.
- Test workflow behaviour.
- Prevent regressions.

### 2.7 Document Export
Technology: Python

Responsibilities:
- Generate downloadable PRD documents.
- Preserve document structure.
- Export reviewed and finalised content.

## 3. Actual Project Structure

```text
AI-PRD-Generator-Fresh/
├── app/
│   └── main.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── PRD.md
├── modules/
│   ├── __init__.py
│   ├── ai_prd_generator.py
│   ├── prd_evaluator.py
│   ├── prd_workspace.py
│   └── schemas.py
├── tests/
│   ├── test_ai_prd_generator.py
│   ├── test_prd_evaluator.py
│   └── test_schemas.py
├── .env
├── .gitignore
└── requirements.txt
```

## 4. AI Generation Workflow

1. Receive product idea and context.
2. Validate the input.
3. Analyse the product idea.
4. Generate the problem statement.
5. Generate user stories.
6. Generate acceptance criteria.
7. Suggest success metrics.
8. Assemble the PRD.
9. Validate the generated structure.
10. Present results for user review.
11. Display heuristic evaluation results and warnings.
12. Allow the user to review and edit the PRD.
13. Export reviewed Markdown and structured JSON.

## 5. AI Reliability

The application should:

- Handle model failures.
- Validate structured outputs.
- Identify missing information.
- Avoid unsupported assumptions.
- Communicate uncertainty.
- Allow human review before finalisation.

## 6. Design System

Primary: #0F766E
Light Background: #F4FAF9
Dark Background: #0B1718
Light Surface: #FFFFFF
Dark Surface: #122526

The interface will support light and dark themes.

## 7. Architecture Principles

1. Modular and maintainable code.
2. Separation of responsibilities.
3. Structured AI outputs.
4. Human oversight.
5. Testable components.
6. Cost-conscious model selection.
7. Evidence-based AI evaluation.

## 8. Implementation Sequence

Phase 1: Project configuration.
Phase 2: UI foundation and theme system.
Phase 3: Input and workflow implementation.
Phase 4: AI model integration.
Phase 5: Structured generation and validation.
Phase 6: Editing and export.
Phase 7: Evaluation and automated testing.
Phase 8: Portfolio documentation.

---

Status: Implemented Architecture (with documented limitations)
