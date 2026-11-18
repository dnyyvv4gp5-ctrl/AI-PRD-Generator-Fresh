import pytest

from modules.ai_prd_generator import (
    build_generation_prompt,
    validate_product_context,
)


def test_valid_product_context():
    validate_product_context(
        "Study Planner",
        "An application that helps students organise assignments and deadlines.",
    )


def test_missing_product_name_is_rejected():
    with pytest.raises(ValueError, match="product name"):
        validate_product_context(
            "",
            "An application that helps students organise assignments.",
        )


def test_missing_idea_is_rejected():
    with pytest.raises(ValueError, match="product idea"):
        validate_product_context("Study Planner", "")


def test_very_short_idea_is_rejected():
    with pytest.raises(ValueError, match="more context"):
        validate_product_context("Study Planner", "Planner")


def test_prompt_preserves_user_context():
    prompt = build_generation_prompt(
        product_name="Study Planner",
        idea="An application for managing university deadlines.",
        target_users="University students",
    )
    assert "Study Planner" in prompt
    assert "University students" in prompt
    assert "Do not invent customer research" in prompt
