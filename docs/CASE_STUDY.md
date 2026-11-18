# AI PRD Generator — Product Case Study

## 1. Overview

The AI PRD Generator is an AI-assisted product management tool that transforms an early-stage product idea into a structured Product Requirements Document (PRD).

**Target users:** Junior and aspiring product managers and early-stage founders who need help translating product ideas into actionable requirements.

**Technology:** Python, Streamlit, Google Gemini API, Pydantic, Pytest.

## 2. Problem

Early-stage product ideas are often expressed informally. Turning them into clear problem statements, user stories, acceptance criteria, and measurable outcomes requires structured product thinking.

For junior product managers, this process can be difficult and time-consuming. Incomplete context can also lead to unclear requirements and unsupported assumptions.

## 3. Product Objective

Build an AI-assisted workflow that helps users create a structured first draft of a PRD while preserving human ownership of product decisions.

The application is designed to support product thinking, not replace product managers or stakeholder validation.

## 4. Core User Journey

1. Enter a product name and idea.
2. Provide target users, problem, and proposed solution.
3. Generate a structured PRD using Gemini.
4. Validate the generated response using Pydantic.
5. Review the PRD quality evaluation and warnings.
6. Edit the Markdown draft.
7. Download the reviewed Markdown or structured JSON.

## 5. Key Product Decisions and Trade-offs

### Structured AI output

**Decision:** Use Pydantic models to define the expected PRD structure.

**Reason:** Structured output makes it easier to validate required fields and handle malformed responses.

**Trade-off:** Schema validation confirms structure, not factual correctness or product relevance.

### Human-in-the-loop review

**Decision:** Allow users to review and edit generated content before exporting.

**Reason:** AI-generated requirements may contain assumptions or miss important business context.

**Trade-off:** Users remain responsible for validating requirements with stakeholders.

### Transparent quality evaluation

**Decision:** Use a rule-based heuristic evaluator with six quality dimensions.

**Reason:** It provides immediate, explainable feedback without presenting an AI-generated score as objective truth.

**Trade-off:** Rules cannot fully measure originality, feasibility, factual accuracy, or business value.

### Modular architecture

**Decision:** Separate generation, schemas, workspace rendering, and evaluation.

**Reason:** This improves maintainability and allows individual components to be tested.

## 6. Quality Evaluation Approach

The evaluator assesses six dimensions:

1. Completeness.
2. User-story quality.
3. Acceptance-criteria quality.
4. Success-metric quality.
5. Assumption and uncertainty handling.
6. Risk and mitigation quality.

The evaluator returns a heuristic score, strengths, and warnings.

The score is a review aid. It is not a validated measure of PRD quality.

## 7. Testing Strategy

The project includes automated tests for:

- AI generation behaviour and error handling.
- Pydantic schema validation.
- PRD evaluator scoring and warning behaviour.

The test suite should be executed before release. Test outcomes must be reported using the latest actual test run.

## 8. Responsible AI Considerations

- Generated requirements are proposals, not verified facts.
- Missing information should be reviewed rather than silently assumed.
- API failures and quota limitations should be communicated.
- Human review is required before requirements are treated as final.
- Confidential product information should not be submitted to an external AI service without appropriate approval.

## 9. Current Limitations

- No external market research or source-backed evidence.
- No automated factual verification.
- No persistent multi-user workspace or collaboration.
- No stakeholder approval workflow.
- Rule-based evaluation cannot determine actual business value or feasibility.

## 10. Future Opportunities

Potential improvements include:

- PRD version history and comparison.
- Stakeholder comments and approval.
- Evidence-backed research integration.
- Configurable evaluation criteria.
- Broader end-to-end testing.
- User feedback collection and usability evaluation.

These are proposed extensions, not current features.

## 11. Product Learning

This project demonstrates how generative AI can support early-stage product documentation when paired with structured validation, transparent evaluation, and human oversight.

A useful AI product should not simply generate content. It should help users understand what is known, what remains uncertain, and what needs human review.
