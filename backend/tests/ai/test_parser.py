import pytest

from backend.app.ai.parser import AIResponseParser
from backend.app.enums.risk_level import RiskLevel


def test_parse_normal_response():
    raw_response = """
    **Risk Level:** HIGH

    **Content Analysis:**

    The message claims to be from the Chase Fraud Department.
    It asks the user to verify their identity immediately.

    **Safe Practical Guidance:**

    Do not click on the link.
    Contact Chase directly using a trusted phone number.

    **Reassurance:**

    If you are concerned, contact Chase through an official channel.
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel.HIGH
    assert result.description != ""
    assert result.solution != ""
    assert result.reassurance != ""


def test_parse_bullet_response():
    raw_response = """
    **Overall Risk Level:** High

    **Content Analysis:**

    + The message claims to be from Chase Bank.
    + It asks the user to verify their identity.
    + It contains a suspicious link.

    **Safe Practical Guidance:**

    + Do not click the link.
    + Do not provide sensitive information.
    + Contact Chase directly.

    **Reassurance:**

    + You can verify the message through an official Chase channel.
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel.HIGH
    assert result.description != ""
    assert result.solution != ""
    assert result.reassurance != ""


def test_parse_missing_sections():
    raw_response = """
    **Risk Level:** MEDIUM

    **Content Analysis:**

    The message contains suspicious content.
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel.MEDIUM
    assert result.description != ""


@pytest.mark.parametrize(
    "risk_level",
    [
        "SAFE",
        "LOW",
        "MEDIUM",
        "HIGH",
        "VERY_HIGH",
    ],
)
def test_parse_all_risk_levels(risk_level):
    raw_response = f"""
    **Risk Level:** {risk_level}

    **Content Analysis:**

    This is a test analysis.

    **Safe Practical Guidance:**

    Take appropriate precautions.

    **Reassurance:**

    There is no need to panic.
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel(risk_level)


def test_parse_malformed_response():
    raw_response = "This is completely unstructured AI output."

    result = AIResponseParser.parse(raw_response)

    assert result is not None
    assert result.risk_level is not None