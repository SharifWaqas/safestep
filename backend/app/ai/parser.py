import re

from backend.app.ai.schemas import (
    AIResponseSchema,
    RiskFactorResult,
)
from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel


class AIResponseParser:

    @staticmethod
    def parse(content: str) -> AIResponseSchema:
        risk_level = AIResponseParser._extract_risk_level(content)
        summary = AIResponseParser._extract_summary(content)
        description = AIResponseParser._extract_description(content)
        solution = AIResponseParser._extract_solution(content)
        reassurance = AIResponseParser._extract_reassurance(content)
        risk_factors = AIResponseParser._extract_risk_factors(content)

        return AIResponseSchema(
            summary=summary,
            risk_level=risk_level,
            description=description,
            solution=solution,
            reassurance=reassurance,
            risk_factors=risk_factors,
        )

    @staticmethod
    def _extract_risk_level(content: str) -> RiskLevel:
        normalized = content.replace("*", "").strip()

        match = re.search(
            r"Risk Level\s*:\s*(SAFE|LOW|MEDIUM|HIGH|VERY\s+HIGH)",
            normalized,
            re.IGNORECASE,
        )

        if not match:
            return RiskLevel.MEDIUM

        value = match.group(1).upper().replace(" ", "_")

        return RiskLevel(value)

    @staticmethod
    def _extract_summary(content: str) -> str:
        normalized = content.replace("*", "")

        match = re.search(
            r"Risk Level\s*:\s*(?:SAFE|LOW|MEDIUM|HIGH|VERY\s+HIGH)"
            r"(.*?)(?=Content Analysis\s*:|Suspicious Characteristics\s*:|"
            r"Safe Practical Guidance\s*:|Reassurance\s*:|$)",
            normalized,
            re.IGNORECASE | re.DOTALL,
        )

        if match:
            summary = match.group(1).strip()

            if summary:
                return summary

        first_paragraph = content.strip().split("\n\n")[0].strip()

        if first_paragraph:
            return first_paragraph

        return "Unable to determine a summary."

    @staticmethod
    def _extract_section(
        content: str,
        section_name: str,
        next_sections: list[str],
    ) -> str:
        normalized = content.replace("*", "")

        escaped_section = re.escape(section_name)

        if next_sections:
            next_pattern = "|".join(
                re.escape(section) for section in next_sections
            )

            pattern = (
                rf"{escaped_section}\s*:\s*"
                rf"(.*?)"
                rf"(?={next_pattern}\s*:|$)"
            )
        else:
            pattern = rf"{escaped_section}\s*:\s*(.*)$"

        match = re.search(
            pattern,
            normalized,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return ""

        return match.group(1).strip()

    @staticmethod
    def _extract_description(content: str) -> str:
        description = AIResponseParser._extract_section(
            content=content,
            section_name="Content Analysis",
            next_sections=[
                "Suspicious Characteristics",
                "Safe Practical Guidance",
                "Reassurance",
            ],
        )

        if description:
            return description

        return "Unable to determine a description."

    @staticmethod
    def _extract_solution(content: str) -> str:
        solution = AIResponseParser._extract_section(
            content=content,
            section_name="Safe Practical Guidance",
            next_sections=[
                "Reassurance",
            ],
        )

        if solution:
            return solution

        return "Do not interact with suspicious content. Verify the message through an official channel."

    @staticmethod
    def _extract_reassurance(content: str) -> str:
        reassurance = AIResponseParser._extract_section(
            content=content,
            section_name="Reassurance",
            next_sections=[],
        )

        if reassurance:
            return reassurance

        return "If you are unsure about a message, verify it through an official channel before taking action."

    @staticmethod
    def _extract_risk_factors(
        content: str,
    ) -> list[RiskFactorResult]:

        normalized = content.lower()

        factors: list[RiskFactorResult] = []

        risk_patterns = {
            RiskFactor.URGENCY_LANGUAGE: [
                "urgency",
                "urgent",
                "immediately",
                "immediate action",
                "act now",
                "verify immediately",
                "without delay",
            ],
            RiskFactor.THREAT_LANGUAGE: [
                "threat",
                "suspended",
                "permanent account limitations",
                "account limitations",
                "fraud charges",
                "account at risk",
                "lose access",
            ],
            RiskFactor.CREDENTIAL_REQUEST: [
                "login credentials",
                "password",
                "username",
                "verify your identity",
                "credentials",
                "sign in",
                "log in",
            ],
            RiskFactor.FINANCIAL_REQUEST: [
                "bank account",
                "financial information",
                "credit card",
                "debit card",
                "payment information",
                "banking information",
            ],
            RiskFactor.SUSPICIOUS_LINK: [
                "suspicious link",
                "phishing link",
                "link provided",
                "click on the link",
                "click the link",
            ],
            RiskFactor.SUSPICIOUS_DOMAIN: [
                "suspicious domain",
                "phishing site",
                "phishing website",
                "malicious website",
                "chase-secure-authenticate.com",
            ],
            RiskFactor.BRAND_IMPERSONATION: [
                "claims to be from",
                "claiming to be",
                "impersonat",
                "pretending to be",
            ],
            RiskFactor.LOGIN_FORM: [
                "login form",
                "login page",
                "sign-in page",
                "sign in page",
            ],
            RiskFactor.PAYMENT_REQUEST: [
                "payment",
                "pay now",
                "make a payment",
                "payment request",
            ],
            RiskFactor.REWARD_LANGUAGE: [
                "reward",
                "prize",
                "winner",
                "won",
                "free gift",
            ],
            RiskFactor.UNREALISTIC_PRICE: [
                "too good to be true",
                "unbelievable price",
                "unrealistic price",
                "huge discount",
            ],
        }

        for risk_factor, patterns in risk_patterns.items():

            matched = any(
                pattern in normalized
                for pattern in patterns
            )

            if not matched:
                continue

            factors.append(
                RiskFactorResult(
                    risk_factor=risk_factor,
                    value=0.8,
                    description=(
                        f"Detected indicators related to "
                        f"{risk_factor.value.replace('_', ' ')}."
                    ),
                )
            )

        return factors