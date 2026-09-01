from decimal import Decimal

import pytest

from backend.app.ai.schemas import RiskFactorResult
from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel
from backend.app.services.risk_scoring_service import RiskScoringService


def make_factor(risk_factor: RiskFactor) -> RiskFactorResult:
    return RiskFactorResult(
        risk_factor=risk_factor,
        description="Test risk factor.",
    )


def test_score_individual_factor():
    factors = [
        make_factor(RiskFactor.UNKNOWN_SENDER),
    ]

    scored = RiskScoringService.score_factors(factors)

    assert len(scored) == 1
    assert scored[0].risk_factor == RiskFactor.UNKNOWN_SENDER
    assert scored[0].score == Decimal("0.10")
    assert scored[0].explanation == "Test risk factor."


def test_all_factor_weights_are_defined():
    for risk_factor in RiskFactor:
        assert risk_factor in RiskScoringService.FACTOR_WEIGHTS


def test_calculate_overall_score_with_multiple_factors():
    factors = [
        make_factor(RiskFactor.SUSPICIOUS_LINK),
        make_factor(RiskFactor.URGENCY_LANGUAGE),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    assert score == Decimal("0.40")


def test_score_is_capped_at_one():
    factors = [
        make_factor(RiskFactor.PAYMENT_REQUEST),
        make_factor(RiskFactor.FINANCIAL_REQUEST),
        make_factor(RiskFactor.CREDENTIAL_REQUEST),
        make_factor(RiskFactor.THREAT_LANGUAGE),
        make_factor(RiskFactor.SUSPICIOUS_DOMAIN),
        make_factor(RiskFactor.BRAND_IMPERSONATION),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    assert score == Decimal("1.00")


def test_no_risk_factors_returns_zero():
    score = RiskScoringService.calculate_overall_score([])

    assert score == Decimal("0.00")


def test_duplicate_risk_factors_are_counted_once():
    factors = [
        make_factor(RiskFactor.SUSPICIOUS_LINK),
        make_factor(RiskFactor.SUSPICIOUS_LINK),
        make_factor(RiskFactor.SUSPICIOUS_LINK),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    assert len(scored_factors) == 1

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    assert score == Decimal("0.25")


def test_brand_impersonation_and_suspicious_domain_add_bonus():
    factors = [
        make_factor(RiskFactor.BRAND_IMPERSONATION),
        make_factor(RiskFactor.SUSPICIOUS_DOMAIN),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.30 + 0.30 + 0.15 interaction bonus
    assert score == Decimal("0.75")


def test_suspicious_link_and_credential_request_add_bonus():
    factors = [
        make_factor(RiskFactor.SUSPICIOUS_LINK),
        make_factor(RiskFactor.CREDENTIAL_REQUEST),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.25 + 0.40 + 0.15 interaction bonus
    assert score == Decimal("0.80")


def test_suspicious_domain_and_credential_request_add_bonus():
    factors = [
        make_factor(RiskFactor.SUSPICIOUS_DOMAIN),
        make_factor(RiskFactor.CREDENTIAL_REQUEST),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.30 + 0.40 + 0.15 interaction bonus
    assert score == Decimal("0.85")


def test_threat_and_urgency_add_bonus():
    factors = [
        make_factor(RiskFactor.THREAT_LANGUAGE),
        make_factor(RiskFactor.URGENCY_LANGUAGE),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.35 + 0.15 + 0.10 interaction bonus
    assert score == Decimal("0.60")


def test_financial_request_and_urgency_add_bonus():
    factors = [
        make_factor(RiskFactor.FINANCIAL_REQUEST),
        make_factor(RiskFactor.URGENCY_LANGUAGE),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.45 + 0.15 + 0.10 interaction bonus
    assert score == Decimal("0.70")


def test_payment_request_and_suspicious_link_add_bonus():
    factors = [
        make_factor(RiskFactor.PAYMENT_REQUEST),
        make_factor(RiskFactor.SUSPICIOUS_LINK),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.45 + 0.25 + 0.15 interaction bonus
    assert score == Decimal("0.85")


def test_brand_impersonation_and_credential_request_add_bonus():
    factors = [
        make_factor(RiskFactor.BRAND_IMPERSONATION),
        make_factor(RiskFactor.CREDENTIAL_REQUEST),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # 0.30 + 0.40 + 0.15 interaction bonus
    assert score == Decimal("0.85")


def test_interaction_bonuses_only_apply_when_all_required_factors_exist():
    factors = [
        make_factor(RiskFactor.BRAND_IMPERSONATION),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    assert score == Decimal("0.30")


@pytest.mark.parametrize(
    ("score", "expected_level"),
    [
        (Decimal("0.00"), RiskLevel.SAFE),
        (Decimal("0.19"), RiskLevel.SAFE),
        (Decimal("0.20"), RiskLevel.LOW),
        (Decimal("0.39"), RiskLevel.LOW),
        (Decimal("0.40"), RiskLevel.MEDIUM),
        (Decimal("0.59"), RiskLevel.MEDIUM),
        (Decimal("0.60"), RiskLevel.HIGH),
        (Decimal("0.79"), RiskLevel.HIGH),
        (Decimal("0.80"), RiskLevel.VERY_HIGH),
        (Decimal("1.00"), RiskLevel.VERY_HIGH),
    ],
)
def test_determine_risk_level(
    score: Decimal,
    expected_level: RiskLevel,
):
    result = RiskScoringService.determine_risk_level(score)

    assert result == expected_level


def test_payment_request_alone_is_medium_risk():
    factors = [
        make_factor(RiskFactor.PAYMENT_REQUEST),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    risk_level = RiskScoringService.determine_risk_level(score)

    assert score == Decimal("0.45")
    assert risk_level == RiskLevel.MEDIUM


def test_credential_request_alone_is_medium_risk():
    factors = [
        make_factor(RiskFactor.CREDENTIAL_REQUEST),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    risk_level = RiskScoringService.determine_risk_level(score)

    assert score == Decimal("0.40")
    assert risk_level == RiskLevel.MEDIUM


def test_suspicious_link_alone_is_low_risk():
    factors = [
        make_factor(RiskFactor.SUSPICIOUS_LINK),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    risk_level = RiskScoringService.determine_risk_level(score)

    assert score == Decimal("0.25")
    assert risk_level == RiskLevel.LOW


def test_multiple_warning_signs_raise_risk():
    factors = [
        make_factor(RiskFactor.SUSPICIOUS_LINK),
        make_factor(RiskFactor.URGENCY_LANGUAGE),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    risk_level = RiskScoringService.determine_risk_level(score)

    assert score == Decimal("0.40")
    assert risk_level == RiskLevel.MEDIUM


def test_multiple_interactions_can_stack():
    factors = [
        make_factor(RiskFactor.BRAND_IMPERSONATION),
        make_factor(RiskFactor.SUSPICIOUS_DOMAIN),
        make_factor(RiskFactor.CREDENTIAL_REQUEST),
    ]

    scored_factors = RiskScoringService.score_factors(factors)

    score = RiskScoringService.calculate_overall_score(
        scored_factors
    )

    # Base:
    # 0.30 + 0.30 + 0.40 = 1.00
    #
    # Interaction bonuses would push this above 1.00,
    # but the final score must remain capped.
    assert score == Decimal("1.00")