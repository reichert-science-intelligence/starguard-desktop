"""Test script to check if sidebar HTML is generated correctly"""
from app import app_ui
import re

# Render the UI to HTML string
html = str(app_ui)

# Check if our nav links are in the output
links = re.findall(r'nav_target[^\"]*', html)
print(f'Found {len(links)} nav_target links')

items_divs = html.count('sg-nav-items')
print(f'Found {items_divs} sg-nav-items references')

a_tags = html.count('<a ')
print(f'Found {a_tags} anchor tags total')

# Show a snippet of sidebar HTML (avoid emoji encoding issues)
sidebar_start = html.find('sg-nav-items')
if sidebar_start > 0:
    print('\nSidebar snippet (first 300 chars):')
    snippet = html[sidebar_start:sidebar_start+300]
    # Replace emojis with placeholders to avoid encoding issues
    snippet_clean = snippet.encode('ascii', 'replace').decode('ascii')
    print(snippet_clean)
else:
    print('\nNo sidebar found in HTML')

# Also check for onclick handlers
onclick_count = html.count('onclick')
print(f'\nFound {onclick_count} onclick handlers')

# Check for specific nav items
home_link = html.find('Home')
print(f'\n"Home" text found at position: {home_link}')
