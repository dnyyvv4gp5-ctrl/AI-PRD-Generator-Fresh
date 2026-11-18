from modules.schemas import (
    PRDDocument,
    SuccessMetric,
    UserStory,
)


def sample_prd():
    return PRDDocument(
        product_name="Study Planner",
        executive_summary="A planner for university students.",
        problem_statement="Students struggle to organise deadlines.",
        target_users=["University students"],
        product_goals=["Improve deadline visibility"],
        non_goals=["Replacing university learning platforms"],
        user_stories=[
            UserStory(
                story_id="US-01",
                story="As a student, I want to add deadlines so that I can plan my work.",
                priority="Must have",
                acceptance_criteria=["A student can save a deadline."],
            )
        ],
        acceptance_criteria=["The application displays saved deadlines."],
        success_metrics=[
            SuccessMetric(
                metric_name="Weekly active users",
                definition="Number of unique users active each week.",
                measurement_method="Track weekly unique active accounts.",
                proposed_target=None,
                target_rationale="Establish a baseline before setting a target.",
            )
        ],
        assumptions=["Students have access to a digital device."],
        open_questions=["Should calendar integration be included?"],
        risks_and_mitigations=["Low adoption: validate usability with students."],
    )


def test_valid_prd_schema():
    prd = sample_prd()
    assert prd.product_name == "Study Planner"
    assert len(prd.user_stories) == 1


def test_user_story_has_acceptance_criteria():
    prd = sample_prd()
    assert prd.user_stories[0].acceptance_criteria


def test_metric_can_have_no_proposed_target():
    prd = sample_prd()
    assert prd.success_metrics[0].proposed_target is None
