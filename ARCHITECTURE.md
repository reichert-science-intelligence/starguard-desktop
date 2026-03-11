# StarGuard Desktop — Architecture

## Overview
StarGuard Desktop is a Shiny for Python application for Medicare Advantage
Star Ratings forecasting and HEDIS gap analytics.

## Repo
- GitHub: reichert-science-intelligence/starguard-desktop
- HuggingFace: rreichert-starguard-desktop.hf.space

## Tech Stack
Shiny for Python · Supabase · Claude API · Plotnine · Docker

## Key Modules
- hedis_gap_trail.py — HEDIS gap identification and trail analysis
- cloud_status_badge.py — live compliance status badges
- suppression_banner.py — suppression logic UI
- hitl_admin_view.py — Human-in-the-Loop admin panel

## CI
GitHub Actions: ruff · mypy --strict · pytest · pip-audit
