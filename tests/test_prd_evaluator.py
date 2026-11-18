from modules.schemas import (
    PRDDocument,
    UserStory,
    SuccessMetric,
)
from modules.prd_evaluator import evaluate_prd


def create_sample_prd():
    return PRDDocument(
        product_name="StudyFlow",
        executive_summary="An AI study planner for university students.",
        problem_statement="Students struggle to organise deadlines.",
        target_users=["University students"],
        product_goals=["Organise deadlines"],
        non_goals=["Direct tutoring"],
        user_stories=[
            UserStory(
                story_id="US-01",
                story=(
                    "As a university student, I want to add deadlines, "
                    "so that I can organise my coursework."
                ),
                priority="Must have",
                acceptance_criteria=[
                    "The system saves a deadline when the user submits it."
                ],
            )
        ],
        acceptance_criteria=[
            "The dashboard displays saved deadlines in chronological order."
        ],
        success_metrics=[
            SuccessMetric(
                metric_name="Schedule generation rate",
                definition="Percentage of users generating a schedule.",
                measurement_method="Track successful generation events.",
                proposed_target=None,
                target_rationale="A baseline is required after launch.",
            )
        ],
        assumptions=["Students will enter their deadlines manually."],
        open_questions=["How should schedule conflicts be handled?"],
        risks_and_mitigations=[
            "Risk: Unrealistic schedules. Mitigation: Allow editing."
        ],
    )


def test_evaluation_returns_score_out_of_100():
    result = evaluate_prd(create_sample_prd())

    assert 0 <= result["overall_score"] <= 100
    assert result["maximum_score"] == 100


def test_evaluation_contains_six_dimensions():
    result = evaluate_prd(create_sample_prd())

    assert len(result["dimensions"]) == 6
    assert sum(item["maximum"] for item in result["dimensions"]) == 100


def test_complete_prd_has_no_missing_section_warning():
    result = evaluate_prd(create_sample_prd())

    assert not any(
        "Missing or empty sections" in warning
        for warning in result["warnings"]
    )


def test_empty_open_questions_reduce_uncertainty_score():
    prd = create_sample_prd()
    prd.open_questions = []

    result = evaluate_prd(prd)

    uncertainty = next(
        item for item in result["dimensions"]
        if item["name"] == "Assumption and uncertainty handling"
    )

    assert uncertainty["score"] < uncertainty["maximum"]


def test_vague_acceptance_criteria_generate_warning():
    prd = create_sample_prd()
    prd.acceptance_criteria = ["The system works correctly."]

    result = evaluate_prd(prd)

    assert any(
        "vague acceptance criterion" in warning.lower()
        for warning in result["warnings"]
    )


def test_invalid_user_story_format_generates_warning():
    prd = create_sample_prd()
    prd.user_stories[0].story = "Students need a better study planner."

    result = evaluate_prd(prd)

    assert any(
        "standard" in warning.lower()
        for warning in result["warnings"]
    )


def test_risk_without_mitigation_generates_warning():
    prd = create_sample_prd()
    prd.risks_and_mitigations = [
        "Risk: Unrealistic revision schedules."
    ]

    result = evaluate_prd(prd)

    assert any(
        "mitigation" in warning.lower()
        for warning in result["warnings"]
    )


def test_missing_risks_reduce_risk_quality_score():
    prd = create_sample_prd()
    prd.risks_and_mitigations = []

    result = evaluate_prd(prd)

    risk_dimension = next(
        item for item in result["dimensions"]
        if item["name"] == "Risk and mitigation quality"
    )

    assert risk_dimension["score"] == 0


def test_evaluation_discloses_its_limitations():
    result = evaluate_prd(create_sample_prd())

    assert "does not verify" in result["limitations"]
    assert "grounded in the original product idea" in result["limitations"]
