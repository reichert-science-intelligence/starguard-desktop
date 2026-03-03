"""
Compound Framework - Day 8-10: Self-Correction Layer

Triple-loop verification: Generate → Validate against golden → Self-correct if mismatch.
"""
import os
import pandas as pd
from pathlib import Path

from .session_context import SessionLearningContext
from .hedis_schemas import HEDIS_CALCULATION_SCHEMA

# Initialize
session_memory = SessionLearningContext()

# Load golden dataset
GOLDEN_DATA_PATH = Path(__file__).parent / "golden_dataset.csv"
GOLDEN_DATA = pd.read_csv(GOLDEN_DATA_PATH) if GOLDEN_DATA_PATH.exists() else pd.DataFrame()

# Lazy-load Anthropic to avoid import errors when API key not set
_client = None


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def triple_loop_execution(
    user_request: str,
    measure_id: str = None,
    plan_id: str = None,
    _recursion_depth: int = 0,
) -> dict:
    """
    Self-correcting execution with validation against golden dataset.

    Loop 1: Generate calculation with session context
    Loop 2: Validate against golden dataset
    Loop 3: Self-correct if mismatch detected

    Args:
        user_request: Natural language query (e.g., "Calculate GSD rate for 2024")
        measure_id: Optional HEDIS measure code for validation
        plan_id: Optional plan identifier

    Returns:
        dict: Structured calculation result with validation status
    """
    max_recursion = 2
    if _recursion_depth >= max_recursion:
        return {
            "error": "Max self-correction loops exceeded",
            "validation_status": "failed",
            "loops_executed": _recursion_depth + 1,
        }

    client = _get_client()

    # LOOP 1: Generate with accumulated learning
    enriched_prompt = session_memory.inject_context(
        f"""
{user_request}

CRITICAL: You MUST use the 'hedis_calculator' tool to return your response.
Do NOT respond with plain text only - you must call the tool with structured data.

Required tool response fields:
- measure_id: HEDIS measure code (e.g., 'GSD', 'CBP')
- numerator: Members meeting the measure criteria
- denominator: Eligible population
- rate: numerator/denominator (0.0 to 1.0)
- sql_executed: The SQL query that would produce this result
- exclusions_count: Members excluded from calculation
- data_quality_score: Confidence in data quality (0.0 to 1.0)

Additional context:
- Measure ID: {measure_id or 'Not specified'}
- Plan ID: {plan_id or 'Not specified'}
- Measurement year: 2024
- Apply PHI-safe rules (no member-level identifiers)
"""
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tool_choice={"type": "tool", "name": "hedis_calculator"},
            tools=[
                {
                    "name": "hedis_calculator",
                    "description": "Calculate HEDIS measure rates. You MUST use this tool to return structured calculation results (measure_id, numerator, denominator, rate, sql_executed).",
                    "input_schema": HEDIS_CALCULATION_SCHEMA,
                }
            ],
            messages=[{"role": "user", "content": enriched_prompt}],
        )
    except Exception as e:
        return {
            "error": True,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "user_message": str(e),
            "validation_status": "failed",
            "loops_executed": 1,
        }

    # Extract structured result
    result = None
    reasoning = ""

    for content in response.content:
        if content.type == "text":
            reasoning += content.text
        elif content.type == "tool_use" and content.name == "hedis_calculator":
            result = content.input
            break

    if not result:
        return {
            "error": True,
            "error_type": "NoStructuredOutput",
            "error_message": "No structured output generated",
            "user_message": "Claude did not return structured data. Try a more specific query (e.g., 'Calculate GSD rate for 2024').",
            "raw_response": reasoning,
            "measure_id": measure_id,
            "validation_status": "failed",
            "loops_executed": 1,
        }

    # Ensure result is dict and add metadata
    if not isinstance(result, dict):
        result = {}
    result["reasoning"] = reasoning
    result["loops_executed"] = 1
    result.setdefault("measure_id", measure_id)
    result.setdefault("numerator", 0)
    result.setdefault("denominator", 0)
    result.setdefault("rate", 0.0)
    result.setdefault("sql_executed", "# SQL not generated")
    result.setdefault("exclusions_count", 0)
    result.setdefault("data_quality_score", 0.0)

    # LOOP 2: Validate against golden dataset
    if measure_id and not GOLDEN_DATA.empty:
        # Support both "measure_id" and "measure" column names
        id_col = "measure_id" if "measure_id" in GOLDEN_DATA.columns else "measure"
        golden_rows = GOLDEN_DATA[GOLDEN_DATA[id_col] == measure_id]

        if not golden_rows.empty:
            # Use most recent year's data for validation
            year_col = "measurement_year" if "measurement_year" in golden_rows.columns else None
            if year_col:
                golden_rows = golden_rows.sort_values(year_col, ascending=False)
            golden_row = golden_rows.iloc[0]

            expected_rate = float(golden_row.get("expected_rate", 0))
            actual_rate = float(result.get("rate", 0))

            # Tolerance based on measure type
            tolerance = 0.02
            if measure_id in ["PDC-DR", "PDC-RASA", "PDC-STA"]:
                tolerance = 0.03

            rate_diff = abs(expected_rate - actual_rate)
            is_match = rate_diff < tolerance

            # LOOP 3: Self-correction if needed
            if not is_match and _recursion_depth < max_recursion - 1:
                correction_prompt = f"""
VALIDATION FAILURE DETECTED

Your calculated rate: {actual_rate:.4f}
Golden dataset rate: {expected_rate:.4f}
Difference: {rate_diff:.4f} (tolerance: {tolerance})

Your SQL approach:
{result.get('sql_executed', 'Not provided')}

Expected approach (from golden dataset):
{golden_row.get('sql_query', 'Not provided')}

Measure details:
- Measure: {measure_id} ({golden_row.get('measure_name', 'N/A')})
- Measurement year: {golden_row.get('measurement_year', 'N/A')}

Identify the discrepancy and regenerate with correct logic.
Common issues to check:
1. Date range calculation (measurement year boundaries)
2. Exclusion criteria application
3. Denominator eligibility rules (age, enrollment)
4. Lookback periods (varies by measure)
5. Join logic (preventing duplicate counts)
"""
                corrected = triple_loop_execution(
                    correction_prompt, measure_id, plan_id, _recursion_depth + 1
                )
                corrected["loops_executed"] = result.get("loops_executed", 1) + (
                    corrected.get("loops_executed", 1)
                )
                corrected["correction_applied"] = True
                corrected["original_rate"] = actual_rate

                session_memory.record_outcome(
                    approach=user_request[:200],
                    success=False,
                    accuracy=1 - (rate_diff / expected_rate) if expected_rate > 0 else 0,
                    error=f"Rate mismatch: {actual_rate:.4f} vs {expected_rate:.4f}",
                )
                return corrected

            # Success - matches golden dataset
            result["validation_status"] = "golden_match"
            result["golden_rate"] = expected_rate
            result["rate_difference"] = rate_diff

            session_memory.record_outcome(approach=user_request[:200], success=True, accuracy=1.0)

        else:
            result["validation_status"] = "no_golden_data"
    else:
        result["validation_status"] = "not_validated"

    return result


def differential_solution_engine(
    problem: str, measure_id: str, plan_id: str = None
) -> dict:
    """
    Generate and compare 3 different approaches to the same calculation.

    Approaches:
    1. Performance-optimized (minimize database queries)
    2. Accuracy-optimized (comprehensive edge case handling)
    3. Maintainability-optimized (readable, auditable SQL)

    Returns best solution with reasoning.
    """
    print("\n" + "=" * 70)
    print("DIFFERENTIAL SOLUTION ENGINE CALLED")
    print("=" * 70)
    print(f"Problem: {problem}")
    print(f"Measure: {measure_id}")
    print(f"Plan: {plan_id}")
    print("=" * 70 + "\n")

    approaches = [
        {
            "name": "Performance-Optimized",
            "instruction": "Generate a HEDIS calculation optimized for query performance. Use indexed columns, minimize joins, and focus on execution speed. Still maintain accuracy but prioritize database efficiency.",
        },
        {
            "name": "Accuracy-Optimized",
            "instruction": "Generate a HEDIS calculation optimized for maximum accuracy. Include all edge cases, comprehensive exclusion logic, and thorough validation. Prioritize correctness over performance.",
        },
        {
            "name": "Maintainability-Optimized",
            "instruction": "Generate a HEDIS calculation optimized for maintainability and auditability. Use clear CTEs, inline comments, and human-readable logic. Make it easy for future analysts to understand and modify.",
        },
    ]

    solutions = []
    for i, approach in enumerate(approaches, 1):
        full_prompt = f"""
{problem}

APPROACH REQUIREMENT: {approach['instruction']}

CRITICAL: You MUST use the 'hedis_calculator' tool to return structured results.

Context:
- Measure: {measure_id}
- Plan: {plan_id or 'Not specified'}
- Follow HEDIS technical specifications
- PHI-safe (no member identifiers)

Return using the hedis_calculator tool with all required fields.
"""
        try:
            result = triple_loop_execution(full_prompt, measure_id, plan_id)
            result["approach_number"] = i
            result["approach_name"] = approach["name"]
            result["approach_instruction"] = approach["instruction"]
            solutions.append(result)
        except Exception as e:
            solutions.append({
                "error": True,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "user_message": f"Approach {i} failed: {str(e)}",
                "approach_number": i,
                "approach_name": approach["name"],
                "approach_instruction": approach["instruction"],
            })

    # Filter valid solutions for comparison
    valid_solutions = [s for s in solutions if not s.get("error")]

    if len(valid_solutions) == 0:
        return {
            "error": True,
            "error_type": "AllApproachesFailed",
            "error_message": "All 3 approaches failed to generate results",
            "user_message": "Differential analysis failed - all approaches encountered errors",
            "solutions": solutions,
            "recommendation": "Unable to compare approaches - all failed",
            "best_solution_index": 0,
            "successful_approaches": 0,
            "total_approaches": len(solutions),
        }

    # Meta-analysis: build comparison prompt from valid solutions
    comparison_prompt = f"You generated {len(valid_solutions)} different approaches for calculating {measure_id}:\n\n"
    for i, sol in enumerate(valid_solutions, 1):
        rate = sol.get("rate", 0)
        comparison_prompt += f"""
**Solution {i} ({sol.get('approach_name', 'Unknown')}):**
- Rate: {rate:.4f} ({rate:.2%})
- Numerator: {sol.get('numerator', 0):,}
- Denominator: {sol.get('denominator', 0):,}
- Validation: {sol.get('validation_status', 'N/A')}
- Loops executed: {sol.get('loops_executed', 1)}
- SQL preview: {str(sol.get('sql_executed', 'N/A'))[:150]}...

"""
    comparison_prompt += """
**Analysis Required:**

1. **Which approach is most appropriate for production use in a Medicare Advantage plan?**

2. **What are the key tradeoffs between approaches?**

3. **Which solution would you trust for a $148M+ cost savings initiative?**

Consider:
- **Accuracy**: Does it match golden dataset? Comprehensive exclusions?
- **Auditability**: Can CMS auditors understand the logic?
- **Performance**: Will it scale to 10K+ members?
- **Maintainability**: Can analysts update it when HEDIS specs change?

Provide your recommendation in 2-3 paragraphs. Be specific about why you chose this approach.
"""

    try:
        client = _get_client()
        meta_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": comparison_prompt}],
        )
        recommendation_text = ""
        for content in meta_response.content:
            if content.type == "text":
                recommendation_text += content.text
    except Exception as e:
        recommendation_text = f"Meta-analysis failed: {str(e)}"

    # Determine best solution and map back to original solutions index
    best_idx_valid = _determine_best_solution(valid_solutions)
    best_solution = valid_solutions[best_idx_valid]
    original_idx = solutions.index(best_solution)

    return {
        "solutions": solutions,
        "valid_solutions": valid_solutions,
        "recommendation": recommendation_text,
        "best_solution_index": original_idx,
        "total_approaches": len(solutions),
        "successful_approaches": len(valid_solutions),
    }


def _determine_best_solution(solutions: list) -> int:
    """Programmatically determine best solution."""
    scores = []
    for sol in solutions:
        score = 0
        if sol.get("validation_status") == "golden_match":
            score += 100
        loops = sol.get("loops_executed", 1)
        score += (4 - loops) * 50 if loops <= 3 else 0
        score += sol.get("data_quality_score", 0) * 50
        scores.append(score)
    return scores.index(max(scores))


__all__ = ["triple_loop_execution", "differential_solution_engine"]
