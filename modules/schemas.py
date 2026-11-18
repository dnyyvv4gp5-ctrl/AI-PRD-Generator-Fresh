from pydantic import BaseModel, Field


class UserStory(BaseModel):
    story_id: str = Field(description="Unique identifier such as US-01")
    story: str = Field(description="A user story in As a... I want... so that... format")
    priority: str = Field(description="Proposed priority: Must have, Should have, or Could have")
    acceptance_criteria: list[str] = Field(
        description="Specific, testable conditions for this user story"
    )


class SuccessMetric(BaseModel):
    metric_name: str = Field(description="Name of the product success metric")
    definition: str = Field(description="What the metric measures")
    measurement_method: str = Field(description="How the metric could be measured")
    proposed_target: str | None = Field(
        description="A proposed target only when reasonably supported. Otherwise null."
    )
    target_rationale: str = Field(
        description="Explain the basis for the target or why a baseline is needed first"
    )


class PRDDocument(BaseModel):
    product_name: str
    executive_summary: str
    problem_statement: str
    target_users: list[str]
    product_goals: list[str]
    non_goals: list[str]
    user_stories: list[UserStory]
    acceptance_criteria: list[str]
    success_metrics: list[SuccessMetric]
    assumptions: list[str]
    open_questions: list[str]
    risks_and_mitigations: list[str]


