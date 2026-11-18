"""Transparent, rule-based evaluation of generated PRD documents."""

import re

from modules.schemas import PRDDocument


def _score(checks: list[bool], maximum: int) -> int:
    """Calculate a proportional score for a group of checks."""
    if not checks:
        return 0
    return round(maximum * sum(checks) / len(checks))


def evaluate_prd(prd: PRDDocument) -> dict:
    """Evaluate PRD structure and basic product-quality signals."""

    warnings = []
    strengths = []

    # 1. Completeness: 15 points
    required_fields = {
        "Executive summary": prd.executive_summary,
        "Problem statement": prd.problem_statement,
        "Target users": prd.target_users,
        "Product goals": prd.product_goals,
        "Non-goals": prd.non_goals,
        "User stories": prd.user_stories,
        "Acceptance criteria": prd.acceptance_criteria,
        "Success metrics": prd.success_metrics,
        "Assumptions": prd.assumptions,
        "Open questions": prd.open_questions,
        "Risks and mitigations": prd.risks_and_mitigations,
    }

    populated = [
        bool(value) if isinstance(value, list)
        else bool(value and value.strip())
        for value in required_fields.values()
    ]

    completeness = _score(populated, 15)
    missing = [
        name for name, present in zip(required_fields, populated)
        if not present
    ]

    if missing:
        warnings.append(
            "Missing or empty sections: " + ", ".join(missing)
        )
    else:
        strengths.append("All required PRD sections are populated.")

    # 2. User-story quality: 15 points
    story_checks = []

    for story in prd.user_stories:
        story_text = story.story.strip().lower()

        valid_format = bool(
            re.search(
                r"^as an? .+,\s*i want .+,\s*so that .+",
                story_text,
            )
        )
        valid_priority = story.priority.lower() in {
            "must have", "should have", "could have"
        }
        has_criteria = bool(story.acceptance_criteria)

        story_checks.extend([
            valid_format,
            valid_priority,
            has_criteria,
        ])

        if not valid_format:
            warnings.append(
                f"{story.story_id}: User story does not follow "
                "the standard As a / I want / so that format."
            )

        if not valid_priority:
            warnings.append(
                f"{story.story_id}: Priority is not a recognised "
                "Must have, Should have, or Could have value."
            )

        if not has_criteria:
            warnings.append(
                f"{story.story_id}: No acceptance criteria provided."
            )

    story_quality = _score(story_checks, 15)

    if story_checks and all(story_checks):
        strengths.append("All user stories follow the required structure.")

    if not prd.user_stories:
        warnings.append("No user stories are available to evaluate.")

    # 3. Acceptance-criteria quality: 25 points
    vague_phrases = (
        "works correctly",
        "user friendly",
        "easy to use",
        "as expected",
        "properly",
        "efficiently",
        "quickly",
        "seamlessly",
    )

    action_pattern = (
        r"\b(can|must|should|displays|shows|saves|creates|"
        r"returns|prevents|rejects|contains|within|equals|"
        r"records|allows|requires|generates|validates|"
        r"updates|deletes|accepts|rejects)\b"
    )

    all_criteria = list(prd.acceptance_criteria)
    for story in prd.user_stories:
        all_criteria.extend(story.acceptance_criteria)

    criteria_checks = []

    for criterion in all_criteria:
        text = criterion.strip().lower()

        has_action = bool(re.search(action_pattern, text))
        is_not_vague = not any(
            phrase in text for phrase in vague_phrases
        )
        is_descriptive = len(text.split()) >= 5

        criteria_checks.extend([
            has_action,
            is_not_vague,
            is_descriptive,
        ])

        if not is_not_vague:
            warnings.append(
                f"Potentially vague acceptance criterion: {criterion}"
            )

        if not has_action or not is_descriptive:
            warnings.append(
                "Review whether this criterion is specific and testable: "
                f"{criterion}"
            )

    criteria_quality = _score(criteria_checks, 25)

    if criteria_checks and all(criteria_checks):
        strengths.append(
            "Acceptance criteria pass the basic specificity checks."
        )

    if not all_criteria:
        warnings.append("No acceptance criteria are available to evaluate.")

    # 4. Success-metric quality: 15 points
    metric_checks = []

    for metric in prd.success_metrics:
        has_target_rationale = bool(metric.target_rationale.strip())

        metric_checks.extend([
            bool(metric.metric_name.strip()),
            bool(metric.definition.strip()),
            bool(metric.measurement_method.strip()),
            has_target_rationale,
        ])

        if metric.proposed_target is not None and not has_target_rationale:
            warnings.append(
                f"{metric.metric_name}: Proposed target needs a rationale."
            )

    metric_quality = _score(metric_checks, 15)

    if metric_checks and all(metric_checks):
        strengths.append(
            "Success metrics include definitions and measurement methods."
        )

    if not prd.success_metrics:
        warnings.append("No success metrics have been defined.")

    # 5. Assumption and uncertainty handling: 15 points
    uncertainty_checks = [
        bool(prd.assumptions),
        bool(prd.open_questions),
    ]

    uncertainty_quality = _score(uncertainty_checks, 15)

    if not prd.assumptions:
        warnings.append(
            "Identify assumptions that still require validation."
        )

    if not prd.open_questions:
        warnings.append("Identify unresolved product questions.")

    if all(uncertainty_checks):
        strengths.append(
            "Assumptions and open questions are explicitly identified."
        )

    # 6. Risk and mitigation quality: 15 points
    risk_checks = []

    for risk in prd.risks_and_mitigations:
        text = risk.strip().lower()

        identifies_risk = "risk" in text
        identifies_mitigation = any(
            term in text
            for term in ("mitigation", "mitigate", "reduce", "prevent")
        )

        risk_checks.extend([
            identifies_risk,
            identifies_mitigation,
        ])

        if not identifies_risk:
            warnings.append(
                f"Clearly identify the risk in this entry: {risk}"
            )

        if not identifies_mitigation:
            warnings.append(
                f"Add a clear mitigation to this risk: {risk}"
            )

    risk_quality = _score(risk_checks, 15)

    if risk_checks and all(risk_checks):
        strengths.append(
            "Documented risks include corresponding mitigation actions."
        )

    if not prd.risks_and_mitigations:
        warnings.append("No product risks or mitigations have been defined.")

    dimensions = [
        {"name": "Completeness", "score": completeness, "maximum": 15},
        {"name": "User-story quality", "score": story_quality, "maximum": 15},
        {
            "name": "Acceptance-criteria quality",
            "score": criteria_quality,
            "maximum": 25,
        },
        {
            "name": "Success-metric quality",
            "score": metric_quality,
            "maximum": 15,
        },
        {
            "name": "Assumption and uncertainty handling",
            "score": uncertainty_quality,
            "maximum": 15,
        },
        {
            "name": "Risk and mitigation quality",
            "score": risk_quality,
            "maximum": 15,
        },
    ]

    overall_score = sum(item["score"] for item in dimensions)

    return {
        "overall_score": overall_score,
        "maximum_score": 100,
        "dimensions": dimensions,
        "strengths": strengths,
        "warnings": list(dict.fromkeys(warnings)),
        "evaluation_type": "Rule-based heuristic evaluation",
        "limitations": (
            "This evaluation checks document completeness and basic "
            "quality signals using predefined rules. It does not verify "
            "whether requirements are factually accurate, whether claims "
            "are supported by external research, or whether the PRD is "
            "grounded in the original product idea. Human review and "
            "stakeholder validation remain necessary."
        ),
    }
