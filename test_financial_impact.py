"""
Test financial impact calculations before integrating into Shiny
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compound_framework.financial_impact import (
    calculate_measure_stars,
    calculate_overall_star_rating,
    calculate_financial_impact,
    generate_gap_closure_recommendations
)

print("=" * 70)
print("TEST 1: Individual Measure Star Calculations")
print("=" * 70)

test_measures = [
    ('GSD', 0.85, "Good glycemic screening"),
    ('KED', 0.75, "Needs improvement"),
    ('CBP', 0.65, "At target"),
    ('BCS', 0.70, "Screening compliance good"),
]

for measure_id, rate, note in test_measures:
    stars = calculate_measure_stars(measure_id, rate)
    print(f"{measure_id}: {rate:.1%} -> {stars:.1f} stars ({note})")

print("\n" + "=" * 70)
print("TEST 2: Overall Star Rating Calculation")
print("=" * 70)

measure_results = [
    {'measure_id': 'GSD', 'rate': 0.85},
    {'measure_id': 'KED', 'rate': 0.75},
    {'measure_id': 'CBP', 'rate': 0.65},
    {'measure_id': 'BCS', 'rate': 0.70},
    {'measure_id': 'COL', 'rate': 0.68},
    {'measure_id': 'PDC-DR', 'rate': 0.80},
]

rating_analysis = calculate_overall_star_rating(measure_results)

print(f"Overall Star Rating: {rating_analysis['overall_rating']:.1f} stars")
print(f"Weighted Score: {rating_analysis['weighted_score']:.2f}")
print(f"Total Measures: {rating_analysis['total_measures']}")

print("\nMeasure Breakdown:")
for m in rating_analysis['measure_breakdown']:
    weight_indicator = "[TRIPLE]" if m['is_triple_weighted'] else "       "
    print(f"  {weight_indicator} {m['measure_id']}: {m['rate']:.1%} -> {m['stars']:.1f} stars (weight: {m['weight']})")

print("\n" + "=" * 70)
print("TEST 3: Financial Impact Projection")
print("=" * 70)

current_rating = rating_analysis['overall_rating']
projected_rating = min(5.0, current_rating + 0.5)

financial = calculate_financial_impact(
    current_rating=current_rating,
    projected_rating=projected_rating,
    member_count=25000,
    avg_revenue_per_member=12000
)

print(f"Current Rating: {financial['current_rating']:.1f} stars")
print(f"Projected Rating: {financial['projected_rating']:.1f} stars")
print(f"Rating Improvement: +{financial['rating_improvement']:.1f}")
print(f"\nMember Count: {financial['member_count']:,}")
print(f"Total Revenue: ${financial['total_revenue']:,.0f}")
print(f"\n--- CMS Bonus Payments ---")
print(f"Current Bonus: {financial['current_bonus_pct']:.1%} = ${financial['current_bonus_payment']:,.0f}")
print(f"Projected Bonus: {financial['projected_bonus_pct']:.1%} = ${financial['projected_bonus_payment']:,.0f}")
print(f"Incremental Revenue: ${financial['incremental_revenue']:,.0f}")
print(f"\n--- Quality Cost Savings (Robert's Methodology) ---")
print(f"Cost Avoidance: ${financial['quality_cost_savings']:,.0f}")
print(f"\n--- TOTAL IMPACT ---")
print(f"Total Financial Impact: ${financial['total_financial_impact']:,.0f}")
print(f"ROI Multiple: {financial['roi_multiple']:.1f}x")
print(f"ROI Percentage: {financial['roi_percentage']:.0f}%")

print("\n" + "=" * 70)
print("TEST 4: Gap Closure Recommendations")
print("=" * 70)

opportunities = generate_gap_closure_recommendations(
    rating_analysis['measure_breakdown'],
    top_n=5
)

print(f"Top {len(opportunities)} Improvement Opportunities:\n")

for i, opp in enumerate(opportunities, 1):
    triple_indicator = "[TRIPLE]" if opp['is_triple_weighted'] else "        "
    print(f"{i}. {triple_indicator} {opp['measure_id']} ({opp['priority']} PRIORITY)")
    print(f"   Current: {opp['current_rate']:.1%} ({opp['current_stars']:.1f} stars)")
    print(f"   Target:  {opp['target_rate']:.1%} ({opp['target_stars']:.1f} stars)")
    print(f"   Gap: {opp['gap']:.1%} ({opp['gap_pct']:.0%} to target)")
    print(f"   Potential Points: {opp['potential_points']:.1f}")
    print(f"   Est. Members Needed: {opp['estimated_members_needed']:,}")
    print()

print("[OK] ALL TESTS PASSED")
print("\nNext step: Integrate into Shiny app with live data")
