import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from modules.schemas import PRDDocument


load_dotenv()

DEFAULT_MODEL = "gemini-3.8-flash"


class PRDGenerationError(Exception):
    """Raised when PRD generation fails or returns invalid output."""


def validate_product_context(
    product_name: str,
    idea: str,
) -> None:
    """Validate the minimum information required to generate a PRD."""

    if not product_name or not product_name.strip():
        raise ValueError("Please provide a product name.")

    if not idea or not idea.strip():
        raise ValueError("Please describe your product idea.")

    if len(idea.strip()) < 20:
        raise ValueError(
            "Please provide a little more context. "
            "Your product idea should contain at least 20 characters."
        )


def build_generation_prompt(
    product_name: str,
    idea: str,
    target_users: str = "",
    problem: str = "",
    solution: str = "",
) -> str:
    """Build a grounded prompt from the user's product context."""

    return f"""
Create a structured Product Requirements Document (PRD).

PRODUCT CONTEXT
Product name: {product_name}
Product idea: {idea}
Target users: {target_users or "Not provided"}
Problem description: {problem or "Not provided"}
Proposed solution: {solution or "Not provided"}

PRODUCT MANAGEMENT INSTRUCTIONS

1. Create a clear, concise, practical PRD for an early-stage product.
2. Preserve the user's stated product intent.
3. Do not invent customer research, market statistics, business results,
   technical capabilities, integrations, or stakeholder decisions.
4. Separate user-provided facts from assumptions.
5. Put important missing information in open_questions.
6. User stories must follow:
   As a [user], I want [capability], so that [benefit].
7. Acceptance criteria must be specific and testable.
8. Propose relevant, measurable success metrics.
9. Do not invent numeric metric targets without a defensible basis.
   Use null for proposed_target when a baseline is required.
10. Identify realistic product risks and practical mitigations.
11. Keep goals distinct from non-goals.
12. Use clear language suitable for a junior product manager
    presenting the PRD to a product and engineering team.

Return only information supported by the context or clearly identified
as a proposal, assumption, or open question.
"""


def generate_prd(
    product_name: str,
    idea: str,
    target_users: str = "",
    problem: str = "",
    solution: str = "",
) -> PRDDocument:
    """Generate and validate a structured PRD using Gemini."""

    validate_product_context(product_name, idea)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise PRDGenerationError(
            "Gemini API key not found. Check your local .env file."
        )

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

    prompt = build_generation_prompt(
        product_name=product_name,
        idea=idea,
        target_users=target_users,
        problem=problem,
        solution=solution,
    )

    for attempt in range(3):
        try:
            client = genai.Client(api_key=api_key)

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=PRDDocument,
                        temperature=0.2,
                        max_output_tokens=5000,
                    ),
                )
            finally:
                client.close()

            if getattr(response, "parsed", None) is not None:
                parsed = response.parsed
                if isinstance(parsed, PRDDocument):
                    return parsed
                return PRDDocument.model_validate(parsed)

            if not response.text:
                raise PRDGenerationError(
                    "Gemini returned an empty response. Please try again."
                )

            return PRDDocument.model_validate_json(response.text)

        except PRDGenerationError:
            raise

        except Exception as exc:
            message = str(exc)
            upper_message = message.upper()

            if "429" in message or "RESOURCE_EXHAUSTED" in upper_message:
                raise PRDGenerationError(
                    "Gemini usage limit reached. Check your AI Studio quota "
                    "and try again later."
                ) from exc

            transient_error = any(
                marker in upper_message
                for marker in (
                    "503",
                    "UNAVAILABLE",
                    "500",
                    "INTERNAL",
                    "502",
                    "BAD_GATEWAY",
                    "504",
                    "DEADLINE_EXCEEDED",
                )
            )

            if transient_error and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            if transient_error:
                raise PRDGenerationError(
                    "Gemini is temporarily experiencing high demand. "
                    "We tried three times but could not complete your PRD. "
                    "Please wait a little and try again."
                ) from exc

            raise PRDGenerationError(
                f"PRD generation failed: {message}"
            ) from exc
