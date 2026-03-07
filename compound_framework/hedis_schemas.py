"""
Compound Framework - Day 5-7: Structured Output Schemas

Force Claude to return data in your proven format. Attach to Claude API calls in Week 2.
"""

# HEDIS calculation output (plan_performance / measure rate structure)
HEDIS_CALCULATION_SCHEMA = {
    "type": "object",
    "properties": {
        "measure_id": {
            "type": "string",
            "enum": [
                "GSD",
                "KED",
                "EED",
                "PDC-DR",
                "BPD",
                "CBP",
                "SUPD",
                "PDC-RASA",
                "PDC-STA",
                "BCS",
                "COL",
                "HEI",
            ],
            "description": "HEDIS measure code",
        },
        "numerator": {
            "type": "integer",
            "minimum": 0,
            "description": "Members meeting measure criteria",
        },
        "denominator": {"type": "integer", "minimum": 1, "description": "Eligible population"},
        "rate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Calculated rate (numerator/denominator)",
        },
        "exclusions_count": {"type": "integer", "minimum": 0},
        "data_quality_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Confidence in data completeness",
        },
        "sql_executed": {
            "type": "string",
            "description": "The SQL query that produced this result",
        },
        "validation_status": {
            "type": "string",
            "enum": ["golden_match", "within_tolerance", "needs_review"],
        },
    },
    "required": ["measure_id", "numerator", "denominator", "rate", "sql_executed"],
}

# Star Rating calculation output (for ROI/demo scenarios)
STAR_RATING_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_rating": {"type": "number", "minimum": 1, "maximum": 5, "multipleOf": 0.5},
        "domain_scores": {
            "type": "object",
            "properties": {
                "staying_healthy": {"type": "number"},
                "managing_chronic": {"type": "number"},
                "member_experience": {"type": "number"},
            },
        },
        "improvement_opportunities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "measure": {"type": "string"},
                    "current_rate": {"type": "number"},
                    "benchmark_50th": {"type": "number"},
                    "gap": {"type": "number"},
                    "potential_points": {"type": "number"},
                },
            },
        },
        "projected_revenue_impact": {
            "type": "number",
            "description": "Based on documented methodologies",
        },
    },
    "required": ["overall_rating", "domain_scores", "improvement_opportunities"],
}
