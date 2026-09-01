from decimal import Decimal

from backend.app.ai.schemas import RiskFactorResult
from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel


class ScoredRiskFactor:

    def __init__(
        self,
        risk_factor: RiskFactor,
        score: Decimal,
        explanation: str,
    ) -> None:
        self.risk_factor = risk_factor
        self.score = score
        self.explanation = explanation


class RiskScoringService:

    FACTOR_WEIGHTS: dict[RiskFactor, Decimal] = {
        RiskFactor.UNKNOWN_SENDER: Decimal("0.10"),
        RiskFactor.REWARD_LANGUAGE: Decimal("0.10"),
        RiskFactor.URGENCY_LANGUAGE: Decimal("0.15"),
        RiskFactor.UNREALISTIC_PRICE: Decimal("0.15"),

        RiskFactor.SUSPICIOUS_LINK: Decimal("0.25"),
        RiskFactor.SUSPICIOUS_DOMAIN: Decimal("0.30"),
        RiskFactor.BRAND_IMPERSONATION: Decimal("0.30"),

        RiskFactor.THREAT_LANGUAGE: Decimal("0.35"),
        RiskFactor.LOGIN_FORM: Decimal("0.35"),
        RiskFactor.CREDENTIAL_REQUEST: Decimal("0.40"),

        RiskFactor.FINANCIAL_REQUEST: Decimal("0.45"),
        RiskFactor.PAYMENT_REQUEST: Decimal("0.45"),
    }

    INTERACTION_BONUSES: tuple[
        tuple[set[RiskFactor], Decimal, str],
        ...
    ] = (
        (
            {
                RiskFactor.BRAND_IMPERSONATION,
                RiskFactor.SUSPICIOUS_DOMAIN,
            },
            Decimal("0.15"),
            "Brand impersonation combined with a suspicious domain.",
        ),
        (
            {
                RiskFactor.SUSPICIOUS_LINK,
                RiskFactor.CREDENTIAL_REQUEST,
            },
            Decimal("0.15"),
            "A suspicious link is combined with a request for credentials.",
        ),
        (
            {
                RiskFactor.SUSPICIOUS_DOMAIN,
                RiskFactor.CREDENTIAL_REQUEST,
            },
            Decimal("0.15"),
            "A suspicious domain is combined with a credential request.",
        ),
        (
            {
                RiskFactor.THREAT_LANGUAGE,
                RiskFactor.URGENCY_LANGUAGE,
            },
            Decimal("0.10"),
            "Threatening language is combined with urgency.",
        ),
        (
            {
                RiskFactor.FINANCIAL_REQUEST,
                RiskFactor.URGENCY_LANGUAGE,
            },
            Decimal("0.10"),
            "A financial request is combined with urgency.",
        ),
        (
            {
                RiskFactor.PAYMENT_REQUEST,
                RiskFactor.SUSPICIOUS_LINK,
            },
            Decimal("0.15"),
            "A payment request is combined with a suspicious link.",
        ),
        (
            {
                RiskFactor.BRAND_IMPERSONATION,
                RiskFactor.CREDENTIAL_REQUEST,
            },
            Decimal("0.15"),
            "Brand impersonation is combined with a credential request.",
        ),
    )

    @classmethod
    def score_factor(
        cls,
        risk_factor: RiskFactor,
    ) -> Decimal:
        return cls.FACTOR_WEIGHTS.get(
            risk_factor,
            Decimal("0.10"),
        )

    @classmethod
    def score_factors(
        cls,
        risk_factors: list[RiskFactorResult],
    ) -> list[ScoredRiskFactor]:

        unique_factors: dict[RiskFactor, RiskFactorResult] = {
            factor.risk_factor: factor
            for factor in risk_factors
        }

        return [
            ScoredRiskFactor(
                risk_factor=factor.risk_factor,
                score=cls.score_factor(factor.risk_factor),
                explanation=factor.description,
            )
            for factor in unique_factors.values()
        ]

    @classmethod
    def calculate_overall_score(
        cls,
        risk_factors: list[ScoredRiskFactor],
    ) -> Decimal:

        if not risk_factors:
            return Decimal("0.00")

        factor_set = {
            factor.risk_factor
            for factor in risk_factors
        }

        base_score = sum(
            factor.score
            for factor in risk_factors
        )

        interaction_bonus = Decimal("0.00")

        for required_factors, bonus, _ in cls.INTERACTION_BONUSES:
            if required_factors.issubset(factor_set):
                interaction_bonus += bonus

        total = base_score + interaction_bonus

        return min(
            total,
            Decimal("1.00"),
        ).quantize(Decimal("0.01"))

    @staticmethod
    def determine_risk_level(
        score: Decimal,
    ) -> RiskLevel:

        if score < Decimal("0.20"):
            return RiskLevel.SAFE

        if score < Decimal("0.40"):
            return RiskLevel.LOW

        if score < Decimal("0.60"):
            return RiskLevel.MEDIUM

        if score < Decimal("0.80"):
            return RiskLevel.HIGH

        return RiskLevel.VERY_HIGH