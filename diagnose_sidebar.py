"""Diagnostic script to check sidebar HTML generation"""

from app import app_ui

html_str = str(app_ui)

# Check if nav_target links exist in output
import re

# Check if nav_target links exist in output
count = html_str.count("nav_target")
print(f"nav_target occurrences: {count}")

# Check for sg-nav-items
count2 = html_str.count("sg-nav-items")
print(f"sg-nav-items occurrences: {count2}")

# Find and print the sidebar section
sidebar_idx = html_str.find("sg-sidebar-brand")
if sidebar_idx > 0:
    # Get 3000 chars from that point
    snippet = html_str[sidebar_idx : sidebar_idx + 3000]
    print("\nSIDEBAR HTML (first 3000 chars):")
    # Replace emojis with placeholders to avoid encoding issues
    snippet_clean = snippet.encode("ascii", "replace").decode("ascii")
    print(snippet_clean)

    # Also check for anchor tags
    a_count = snippet.count("<a ")
    print(f"\nAnchor tags in sidebar snippet: {a_count}")

    # Check for onclick handlers
    onclick_count = snippet.count("onclick")
    print(f"onclick handlers in sidebar snippet: {onclick_count}")

    # Count total anchor tags in entire HTML
    total_a = html_str.count("<a ")
    print(f"\nTotal anchor tags in entire HTML: {total_a}")

    # Check if all nav_target values are present
    nav_targets = re.findall(r"nav_target', '([^']+)'", html_str)
    print(f"\nUnique nav_target values found: {len(set(nav_targets))}")
    print(f"nav_target values: {sorted(set(nav_targets))}")
else:
    print("\nERROR: sg-sidebar-brand not found in HTML output")
    # Search for sidebar class
    sidebar_idx2 = html_str.find("sidebar")
    print(f"sidebar found at index: {sidebar_idx2}")
    if sidebar_idx2 > 0:
        snippet2 = html_str[sidebar_idx2 : sidebar_idx2 + 1000]
        snippet2_clean = snippet2.encode("ascii", "replace").decode("ascii")
        print(snippet2_clean)
