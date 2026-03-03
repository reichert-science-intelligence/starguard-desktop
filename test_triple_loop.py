"""
Compound Framework - Day 11: Test Triple-Loop with Real Data

Run from starguard-shiny directory:
    set ANTHROPIC_API_KEY=your-key-here
    python test_triple_loop.py
"""
import os
import sys

# Ensure starguard-shiny is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("ERROR: Set ANTHROPIC_API_KEY environment variable")
    sys.exit(1)

from compound_framework.ai_engine_enhanced import (
    triple_loop_execution,
    differential_solution_engine,
)

print("=" * 60)
print("TEST 1: Single Execution with Golden Validation")
print("=" * 60)

result = triple_loop_execution(
    "Calculate the GSD (Glycemic Screening for Diabetes) rate for measurement year 2024",
    measure_id="GSD",
    plan_id="H1234",
)

if "error" in result:
    print(f"✗ Error: {result['error']}")
else:
    print(f"\n✓ Measure: {result.get('measure_id', 'N/A')}")
    print(f"✓ Numerator: {result.get('numerator', 0):,}")
    print(f"✓ Denominator: {result.get('denominator', 0):,}")
    print(f"✓ Rate: {result.get('rate', 0):.2%}")
    print(f"✓ Validation Status: {result.get('validation_status', 'N/A')}")
    print(f"✓ Loops Executed: {result.get('loops_executed', 1)}")

    if result.get("validation_status") == "golden_match":
        print("✓ PASSED - Matches golden dataset within tolerance")
        print(f"  Golden rate: {result.get('golden_rate', 0):.4f}")
        print(f"  Difference: {result.get('rate_difference', 0):.4f}")
    else:
        print(f"⚠ WARNING - {result.get('validation_status', 'unknown')}")

print("\n" + "=" * 60)
print("TEST 2: Differential Testing (3 Approaches)")
print("=" * 60)

diff_results = differential_solution_engine(
    "Calculate the CBP (Blood Pressure Control) rate with all exclusions",
    measure_id="CBP",
    plan_id="H1234",
)

print(f"\n✓ Generated {len(diff_results['solutions'])} solutions")
print(f"✓ Best solution: #{diff_results['best_solution_index'] + 1}")
print(f"\n{'='*60}")
print("RECOMMENDATION:")
print(diff_results["recommendation"][:800] + "..." if len(diff_results["recommendation"]) > 800 else diff_results["recommendation"])

print("\n✓ ALL TESTS COMPLETED")
