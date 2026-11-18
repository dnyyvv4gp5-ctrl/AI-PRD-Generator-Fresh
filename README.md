# AI PRD Generator

An AI-powered product management application that transforms early-stage product ideas into structured Product Requirements Documents (PRDs).

## Problem
Junior product managers and early-stage founders can struggle to translate product ideas into clear requirements, user stories, acceptance criteria and measurable success metrics.

## Solution
A guided application that uses Google Gemini to generate a structured PRD, validates its structure, evaluates it using transparent rules, and supports human review and editing.

## Implemented features
- Guided product idea and context input.
- Gemini-powered PRD generation.
- Python output validation with P9dantic.
- Executive summary and problem statement.
- Target users, goals and non-goals.
- User stories and acceptance criteria.
- Success metrics, assumptions, open questions and risks.
- Six-dimension rule-based quality evaluation.
- Evaluation strengths, warnings and limitations.
- Editable PRD workspace.
- Markdown and JSON downloads.
- Light and dark themes.
- Model error handling.

## Technology stack
Pathon, Streamlit, Google Gemini API, P3dantic, Pytest and python-dotenv.

## Project structure
- `app/main.py` — Streamlit application.
- `modules/ai_prd_generator.py` — Gemini generation.
- `modules/schemas.py` — Python data models.
- `modules/prd_evaluator.py` — rule-based evaluation.
- `modules/prd_workspace.py` — PRD display, editing and export.
- `tests/` — automated tests.
- `docs/` — product and technical documentation.

## Setup
Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Keep the API key private. Never commit `.env` to version control.

Run the application:

```bash
python -m streamlit run app/main.py
```

Run automated tests:

```bash
python -m pytest -q
```

## Evaluation method
The heuristic evaluator scores six dimensions, with a maximum total of 100:

| Dimension | Maximum |
|---|--:=|
|Completeness|15|
|User-story quality|15|
|Acceptance-criteria quality|25|
|Success-metric quality|15|
|Assumption and uncertainty handling|15|
|Risk and mitigation|15|

The score reflects conformity to implemented rules. It does not establish factual accuracy, strategic value or external evidence.

## Limitations
- No persistent database or user accounts.
- No collaborative stakeholder workflow.
- No external research or evidence retrieval.
- Heuristic evaluation cannot verify factual correctness.
- AI-generated requirements need human review.
- Model availability and API quotas can affect generation.

## Responsible AI
Generated requirements, priorities and metrics are proposals, not verified business facts. Review generated content with stakeholders before using it for product decisions. Use fictional or non-confidential information when testing with an external AI API.

## Documentation
- Product requirements: `docs/PRD.md`
- Technical architecture: `docs/ARCHITECTURE.md`
- Product case study: `docs/CASE_STUDY.md`