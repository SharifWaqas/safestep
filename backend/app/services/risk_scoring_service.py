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
        RiskFactor.UNKNOWN_SENDER: Decimal("0.15"),
        RiskFactor.REWARD_LANGUAGE: Decimal("0.15"),
        RiskFactor.URGENCY_LANGUAGE: Decimal("0.20"),
        RiskFactor.UNREALISTIC_PRICE: Decimal("0.20"),
        RiskFactor.SUSPICIOUS_LINK: Decimal("0.30"),
        RiskFactor.SUSPICIOUS_DOMAIN: Decimal("0.30"),
        RiskFactor.BRAND_IMPERSONATION: Decimal("0.30"),
        RiskFactor.THREAT_LANGUAGE: Decimal("0.60"),
        RiskFactor.LOGIN_FORM: Decimal("0.35"),
        RiskFactor.CREDENTIAL_REQUEST: Decimal("0.60"),
        RiskFactor.FINANCIAL_REQUEST: Decimal("0.60"),
        RiskFactor.PAYMENT_REQUEST: Decimal("0.60"),
    }

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

        return [
            ScoredRiskFactor(
                risk_factor=factor.risk_factor,
                score=cls.score_factor(factor.risk_factor),
                explanation=factor.description,
            )
            for factor in risk_factors
        ]

    @classmethod
    def calculate_overall_score(
        cls,
        risk_factors: list[RiskFactorResult],
    ) -> Decimal:

        if not risk_factors:
            return Decimal("0.00")

        unique_factors = {
            factor.risk_factor
            for factor in risk_factors
        }

        total = sum(
            cls.score_factor(risk_factor)
            for risk_factor in unique_factors
        )

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