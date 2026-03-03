"""
Slim ROI Calculator for Shiny — 3 methods + recommendation only (no DB).
"""
from typing import Dict


def calculate_roi_three_methods(
    investment_amount: float,
    expected_closures: int,
    revenue_per_closure: float = 100.0,
    membership: int = 1000,
    quality_bonus_per_star: float = 50.0,
) -> Dict:
    """
    Calculate ROI using three methodologies.
    Method 1: Conservative (direct only). Method 2: Comprehensive (indirect). Method 3: CMS-Focused.
    """
    rev_direct = expected_closures * revenue_per_closure
    inv = max(investment_amount, 1.0)
    admin_savings = inv * 0.15
    star_bonus_proxy = membership * quality_bonus_per_star * 0.5
    stars_equivalent = min(5, max(0, (expected_closures / max(membership * 0.01, 1)) * 10))
    cms_bonus = membership * quality_bonus_per_star * (stars_equivalent * 0.2)

    m1_benefit = rev_direct
    m2_benefit = rev_direct + admin_savings + star_bonus_proxy
    m3_benefit = rev_direct + cms_bonus

    return {
        "method_1_conservative": {
            "net_roi": m1_benefit - inv,
            "roi_ratio": m1_benefit / inv if inv else 0,
            "total_benefit": m1_benefit,
            "description": "Direct cost avoidance only. Best for internal reporting.",
        },
        "method_2_comprehensive": {
            "net_roi": m2_benefit - inv,
            "roi_ratio": m2_benefit / inv if inv else 0,
            "total_benefit": m2_benefit,
            "description": "Includes admin savings and quality bonus. Best for CFO/board.",
        },
        "method_3_cms_focused": {
            "net_roi": m3_benefit - inv,
            "roi_ratio": m3_benefit / inv if inv else 0,
            "total_benefit": m3_benefit,
            "description": "Star Rating bonus emphasis. Best for CMS/CMO.",
        },
    }


def recommend_roi_method(
    org_type: str = "payer",
    audience: str = "CFO",
    reporting: str = "internal",
) -> Dict:
    """Recommend which ROI method to use."""
    if reporting == "CMS" or audience == "CMO":
        return {
            "recommended_method": "method_3_cms_focused",
            "label": "CMS-Focused (Star Rating emphasis)",
            "explanation": "Use for CMS reporting or quality/CMO stakeholders.",
        }
    if audience == "CFO" or reporting == "board":
        return {
            "recommended_method": "method_2_comprehensive",
            "label": "Comprehensive (includes indirect benefits)",
            "explanation": "Use for CFO and board. Full value story.",
        }
    return {
        "recommended_method": "method_1_conservative",
        "label": "Conservative (direct only)",
        "explanation": "Use for internal planning and defensible single-number ROI.",
    }
