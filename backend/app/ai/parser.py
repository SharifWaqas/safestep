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
    def _normalize_content(content: str) -> str:
        return content.replace("*", "").strip()

    @staticmethod
    def _extract_risk_level(content: str) -> RiskLevel:
        normalized = AIResponseParser._normalize_content(content)

        match = re.search(
            r"Scam/Risk Level\s*:\s*"
            r"(SAFE|LOW|MEDIUM|HIGH|VERY[\s_]+HIGH)",
            normalized,
            re.IGNORECASE,
        )

        if not match:
            match = re.search(
                r"Risk Level\s*:\s*"
                r"(SAFE|LOW|MEDIUM|HIGH|VERY[\s_]+HIGH)",
                normalized,
                re.IGNORECASE,
            )

        if not match:
            return RiskLevel.MEDIUM

        value = match.group(1).upper().replace(" ", "_")

        return RiskLevel(value)

    @staticmethod
    def _extract_summary(content: str) -> str:
        normalized = AIResponseParser._normalize_content(content)

        description = AIResponseParser._extract_section(
            content=normalized,
            section_names=[
                "Content Description",
                "Content Analysis",
            ],
            next_sections=[
                "Warning Signs/Suspicious Characteristics",
                "Warning Signs",
                "Suspicious Characteristics",
                "User Action",
                "Recommended Action",
                "Safe Practical Guidance",
                "Reassurance",
                "Additional Tips",
                "Answer",
            ],
        )

        if description:
            sentences = re.split(
                r"(?<=[.!?])\s+",
                description.strip(),
            )

            for sentence in sentences:
                sentence = sentence.strip()

                if sentence:
                    return sentence

        summary = AIResponseParser._extract_section(
            content=normalized,
            section_names=["Summary"],
            next_sections=[
                "Scam/Risk Level",
                "Risk Level",
                "Overall Scam/Risk Level",
                "Content Description",
                "Content Analysis",
                "Warning Signs/Suspicious Characteristics",
                "Warning Signs",
                "Suspicious Characteristics",
                "User Action",
                "Recommended Action",
                "Safe Practical Guidance",
                "Reassurance",
                "Additional Tips",
                "Answer",
            ],
        )

        if summary:
            return summary

        return "Unable to determine a summary."

    @staticmethod
    def _extract_section(
        content: str,
        section_names: list[str],
        next_sections: list[str],
    ) -> str:

        normalized = AIResponseParser._normalize_content(content)

        section_pattern = "|".join(
            re.escape(section)
            for section in section_names
        )

        if next_sections:
            next_pattern = "|".join(
                re.escape(section)
                for section in next_sections
            )

            pattern = (
                rf"(?:{section_pattern})\s*:\s*"
                rf"(.*?)"
                rf"(?=(?:{next_pattern})\s*:|$)"
            )
        else:
            pattern = (
                rf"(?:{section_pattern})\s*:\s*(.*)$"
            )

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
            section_names=[
                "Content Description",
                "Content Analysis",
            ],
            next_sections=[
                "Warning Signs/Suspicious Characteristics",
                "Warning Signs",
                "Suspicious Characteristics",
                "User Action",
                "Recommended Action",
                "Safe Practical Guidance",
                "Reassurance",
                "Additional Tips",
                "Answer",
            ],
        )

        if description:
            return description

        return "Unable to determine a description."

    @staticmethod
    def _extract_solution(content: str) -> str:
        solution = AIResponseParser._extract_section(
            content=content,
            section_names=[
                "User Action",
                "Recommended Action",
                "Safe Practical Guidance",
            ],
            next_sections=[
                "Reassurance",
                "Additional Tips",
                "Answer",
            ],
        )

        if solution:
            return solution

        return (
            "Do not interact with suspicious content. "
            "Verify the message through an official channel."
        )

    @staticmethod
    def _extract_reassurance(content: str) -> str:
        reassurance = AIResponseParser._extract_section(
            content=content,
            section_names=["Reassurance"],
            next_sections=[
                "Additional Tips",
                "Answer",
            ],
        )

        if reassurance:
            return reassurance

        return (
            "If you are unsure about a message, verify it through "
            "an official channel before taking action."
        )

    @staticmethod
    def _looks_like_heading(value: str) -> bool:
        value = value.strip()

        if not value:
            return False

        return bool(
            re.fullmatch(
                r"(Summary|Scam/Risk Level|Risk Level|"
                r"Overall Scam/Risk Level|"
                r"Content Description|Content Analysis|"
                r"Warning Signs/Suspicious Characteristics|"
                r"Warning Signs|Suspicious Characteristics|"
                r"User Action|Recommended Action|"
                r"Safe Practical Guidance|"
                r"Reassurance|Additional Tips|Answer)"
                r"\s*:",
                value,
                re.IGNORECASE,
            )
        )

    @classmethod
    def _extract_risk_factors(
        cls,
        content: str,
    ) -> list[RiskFactorResult]:

        warning_section = cls._extract_section(
            content,
            [
                "Warning Signs/Suspicious Characteristics",
                "Warning Signs",
                "Suspicious Characteristics",
            ],
            [
                "User Action",
                "Recommended Action",
                "Safe Practical Guidance",
                "Reassurance",
                "Additional Tips",
                "Answer",
            ],
        )

        if not warning_section:
            return []

        normalized = warning_section.lower()

        factors: list[RiskFactorResult] = []

        patterns: dict[RiskFactor, list[str]] = {
            RiskFactor.URGENCY_LANGUAGE: [
                "urgent",
                "urgency",
                "immediately",
                "within 24 hours",
                "within 48 hours",
                "act now",
                "limited time",
            ],
            RiskFactor.THREAT_LANGUAGE: [
                "threat",
                "threatening",
                "legal action",
                "arrest",
                "penalty",
                "consequences",
            ],
            RiskFactor.CREDENTIAL_REQUEST: [
                "password",
                "username",
                "credentials",
                "login credentials",
                "verify your identity",
            ],
            RiskFactor.FINANCIAL_REQUEST: [
                "payment",
                "pay",
                "money",
                "financial information",
                "bank account",
                "credit card",
            ],
            RiskFactor.SUSPICIOUS_LINK: [
                "suspicious link",
                "phishing link",
                "malicious link",
                "unknown link",
                "untrusted link",
            ],
            RiskFactor.SUSPICIOUS_DOMAIN: [
                "suspicious domain",
                "malicious domain",
                "fake domain",
                "untrusted domain",
                "does not appear to be a legitimate",
            ],
            RiskFactor.BRAND_IMPERSONATION: [
                "impersonat",
                "pretending to be",
                "claims to be",
                "fake amazon",
                "fake bank",
                "fake chase",
            ],
            RiskFactor.UNKNOWN_SENDER: [
                "unknown sender",
                "sender is unknown",
                "unknown number",
                "unknown phone number",
                "unrecognized sender",
                "unrecognized number",
            ],
            RiskFactor.LOGIN_FORM: [
                "login page",
                "login form",
                "sign in page",
                "sign-in page",
            ],
            RiskFactor.PAYMENT_REQUEST: [
                "requests payment",
                "request payment",
                "demands payment",
                "payment request",
                "asks the user to pay",
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
                "unrealistic price",
                "unbelievable price",
                "huge discount",
                "massive discount",
            ],
        }

        for risk_factor, factor_patterns in patterns.items():

            matched = any(
                pattern in normalized
                for pattern in factor_patterns
            )

            if matched:
                factors.append(
                    RiskFactorResult(
                        risk_factor=risk_factor,
                        description=(
                            f"Detected indicators related to "
                            f"{risk_factor.value.replace('_', ' ')}."
                        ),
                    )
                )

        return factors