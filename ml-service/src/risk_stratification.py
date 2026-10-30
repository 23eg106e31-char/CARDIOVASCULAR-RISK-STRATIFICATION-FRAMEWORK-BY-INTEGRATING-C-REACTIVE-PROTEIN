"""
Clinically Interpretable Cardiovascular Risk Stratification System
------------------------------------------------------------------
Categorizes individuals into Low, Moderate, and High risk groups based on
AI/ML model probability outputs (TabPFN) integrating C-reactive protein (hs-CRP)
and clinical risk factors.
"""

from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np

# ACC/AHA 10-year Event Risk Bands
PROB_LOW_MAX = 0.075       # < 7.5%  -> Low
PROB_HIGH_MIN = 0.20       # > 20%   -> High

# AHA/CDC hs-CRP Categories (mg/L)
CRP_LOW_MAX = 1.0
CRP_HIGH_MIN = 3.0


@dataclass
class RiskResult:
    predicted_probability: float
    base_tier: str
    crp_category: str
    crp_modifier_applied: bool
    final_tier: str
    top_features: List[Tuple[str, float]] = field(default_factory=list)

    def to_dict(self):
        return {
            "predicted_probability": round(self.predicted_probability, 4),
            "base_tier": self.base_tier,
            "crp_category": self.crp_category,
            "crp_modifier_applied": self.crp_modifier_applied,
            "final_tier": self.final_tier,
            "top_features": self.top_features,
        }


def probability_to_tier(prob: float) -> str:
    if prob < PROB_LOW_MAX:
        return "Low"
    elif prob > PROB_HIGH_MIN:
        return "High"
    return "Moderate"


def crp_category(crp_value: float) -> str:
    if crp_value < CRP_LOW_MAX:
        return "Low (<1 mg/L)"
    elif crp_value <= CRP_HIGH_MIN:
        return "Average (1-3 mg/L)"
    return "High (>3 mg/L)"


def apply_crp_modifier(base_tier: str, crp_value: float) -> Tuple[str, bool]:
    """
    Clinical rule: for intermediate (Moderate) risk patients, high CRP (>3 mg/L)
    shifts final risk to High; low CRP (<1 mg/L) shifts risk to Low.
    """
    modifier_applied = False
    tier = base_tier
    if base_tier == "Moderate":
        if crp_value > CRP_HIGH_MIN:
            tier = "High"
            modifier_applied = True
        elif crp_value < CRP_LOW_MAX:
            tier = "Low"
            modifier_applied = True
    return tier, modifier_applied


def stratify(prob: float, crp_value: float, top_features: List[Tuple[str, float]] = None) -> RiskResult:
    base_tier = probability_to_tier(prob)
    crp_cat = crp_category(crp_value)
    final_tier, modifier_applied = apply_crp_modifier(base_tier, crp_value)
    return RiskResult(
        predicted_probability=float(prob),
        base_tier=base_tier,
        crp_category=crp_cat,
        crp_modifier_applied=modifier_applied,
        final_tier=final_tier,
        top_features=top_features or [],
    )


def stratify_batch(probs: np.ndarray, crp_values: np.ndarray) -> List[RiskResult]:
    return [stratify(p, c) for p, c in zip(probs, crp_values)]
