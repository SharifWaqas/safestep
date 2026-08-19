import pytest

from backend.app.ai.parser import AIResponseParser
from backend.app.enums.risk_level import RiskLevel
from backend.app.enums.risk_factor import RiskFactor


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


def test_parse_nvidia_markdown_response():
    raw_response = """
    **Analysis of the Image**

    **Scam/Risk Level:** LOW

    **Content Description:**

    The image shows a text message on an iPhone.
    The message appears to be a phishing attempt because
    it asks the user to click on a link and provide personal information.

    **Warning Signs/Suspicious Characteristics:**

    * The message is from an unknown sender ("AMAZON.CON").
    * The message contains a generic greeting and a sense of urgency.
    * The message requests the user to click on a link to pay a fine.
    * The link may be a phishing link.

    **User Action:**

    * Do not click on the link or provide personal information.
    * Do not respond to the message.
    * Delete the message and report it as spam.

    **Reassurance:**

    Amazon would never send a message like this to its customers.
    This message is likely a phishing attempt.

    **Additional Tips:**

    * Be cautious of generic greetings and urgent requests.
    * Never click on links from unknown senders.

    **Answer:** HIGH
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel.LOW

    assert (
        "text message on an iPhone"
        in result.description
    )

    assert (
        "Do not click on the link"
        in result.solution
    )

    assert (
        "Amazon would never send a message"
        in result.reassurance
    )

    assert "Additional Tips" not in result.reassurance

    assert result.summary != "Warning Signs/"
    assert result.summary != ""


def test_parse_recommended_action():
    raw_response = """
    **Analysis of the Image**

    **Scam/Risk Level:** HIGH

    **Content Description:**

    The message appears to be a phishing attempt.

    **Warning Signs/Suspicious Characteristics:**

    The message contains a suspicious payment request.

    **Recommended Action:**

    Do not click on the link.
    Do not provide personal or financial information.
    Contact Amazon through its official website.

    **Reassurance:**

    You can safely ignore the message and verify it through an official channel.
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel.HIGH
    assert "Do not click on the link." in result.solution
    assert "Contact Amazon" in result.solution
    assert "You can safely ignore" in result.reassurance


def test_parse_real_nvidia_amazon_response():
    raw_response = """
    **Analysis of the Image**

    **Scam/Risk Level:** HIGH

    **Content Description:**

    The message claims that the recipient has been fined $85.22
    for failing to return an order with order number #23442314.
    It requests the recipient to log in to pay the fine or apply
    for a waiver within 48 hours by clicking on a provided link.

    **Warning Signs/Suspicious Characteristics:**

    * The message creates a sense of urgency by giving the recipient
      only 48 hours to respond.
    * The message requests payment of a fine.
    * The message contains a suspicious link.
    * The link does not appear to be a legitimate Amazon URL.

    **User Action:**

    * Do not click on the link.
    * Do not provide personal or financial information.
    * Contact Amazon directly through its official customer service channels.

    **Reassurance:**

    Amazon will not send unsolicited messages demanding payment
    through unverified links.
    """

    result = AIResponseParser.parse(raw_response)

    assert result.risk_level == RiskLevel.HIGH

    assert result.summary != "Unable to determine a summary."
    assert result.summary != ""

    assert result.description != "Unable to determine a description."
    assert result.description != ""

    assert (
        "fined $85.22"
        in result.description
    )

    assert (
        "Do not click on the link"
        in result.solution
    )

    assert (
        "Contact Amazon directly"
        in result.solution
    )

    assert (
        "Amazon will not send unsolicited messages"
        in result.reassurance
    )

def test_parse_does_not_detect_risk_factors_from_guidance():
    raw_response = """
    **Analysis of the Image**

    **Scam/Risk Level:** LOW

    **Content Description:**

    The message is from an unknown sender.

    **Warning Signs/Suspicious Characteristics:**

    The sender is unknown.

    **User Action:**

    Do not click on suspicious links.
    Do not provide sensitive information.

    **Reassurance:**

    You should avoid suspicious links and verify messages
    through an official channel.
    """

    result = AIResponseParser.parse(raw_response)

    risk_factors = {
        factor.risk_factor
        for factor in result.risk_factors
    }

    assert RiskFactor.UNKNOWN_SENDER in risk_factors
    assert RiskFactor.SUSPICIOUS_LINK not in risk_factors