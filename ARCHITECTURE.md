# StarGuard Desktop — Architecture

## Purpose

StarGuard Desktop is a production-grade Medicare Advantage Intelligence Platform for health plan analysts and Star Ratings program managers. It delivers 18+ analytical pages: HEDIS gap analysis, HCC risk stratification, Star Rating forecasting, ROI analytics, HITL Admin View, and AI-powered executive insights. Phase 2 adds gap suppression, suppression banner, HITL Admin View, and Intervention Optimizer.

---

## Component Map (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      StarGuard Desktop (Shiny App)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  app.py (main)                                                               │
│    ├── hedis_gap_trail.py ──────► Google Sheets + Supabase                  │
│    │   └── .gap_suppressions.json (Phase 2)                                 │
│    ├── hedis_gap_ui.py (if present)                                          │
│    ├── cloud_status_badge.py                                                 │
│    ├── suppression_banner.py (Phase 2)                                       │
│    ├── hitl_admin_view.py (Phase 2)                                           │
│    ├── intervention_optimizer.py (Phase 2)                                    │
│    ├── compound_framework/ (AI engine, financial impact)                      │
│    ├── utils/ (formatters, intervention_analysis, roi_calculator)            │
│    └── www/ (static assets, QR codes)                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Module Reference

| Module | Role |
|--------|------|
| `app.py` | Main Shiny UI + server, 18+ pages |
| `hedis_gap_trail.py` | HEDIS gap CRUD, Google Sheets, Supabase, Phase 2 gap suppression |
| `hedis_gap_ui.py` | HEDIS gap panel UI (if present) |
| `cloud_status_badge.py` | Cloud services badge |
| `suppression_banner.py` | Phase 2 gap suppression banner |
| `hitl_admin_view.py` | Phase 2 HITL Admin View (gap suppressions) |
| `intervention_optimizer.py` | Phase 2 intervention optimizer |
| `compound_framework/` | AI engine, financial impact, gap closure |
| `utils/` | Formatters, intervention analysis, ROI calculator |

---

## Data Flow

```
User → Shiny UI → Server Handlers
         │
         ├──► hedis_gap_trail.push_hedis_gap() → Google Sheets + Supabase
         ├──► hedis_gap_trail.fetch_hedis_gaps() → DataFrame (suppression filter)
         ├──► get_gap_suppressions() → .gap_suppressions.json
         ├──► add/remove_gap_suppression() → JSON CRUD
         ├──► apply_gap_suppression_filter() → filter DataFrame
         └──► compound_framework, utils → AI, ROI, interventions
```

---

## Deployment Topology

| Environment | Host | Port | Entry |
|-------------|------|------|-------|
| Local | localhost | 7860 | `shiny run app.py` |
| HuggingFace Spaces | rreichert/starguard-desktop | 7860 | Docker, shiny run app.py |
| Docker | python:3.11-slim | 7860 | `shiny run app.py` |

---

## Dependency Graph

```
app.py
  ├── shiny, shinywidgets, htmltools
  ├── hedis_gap_trail, cloud_status_badge
  ├── suppression_banner, hitl_admin_view, intervention_optimizer
  ├── compound_framework, utils
  ├── pandas, numpy, plotly
  └── gspread, supabase, google-auth, anthropic
```

---

## Configuration

| Variable | Purpose |
|----------|---------|
| `GSHEETS_CREDS_JSON` | Google Sheets credentials (HF Secret) |
| `HEDIS_SHEET_ID` | Sheet name (default: StarGuard_HEDIS_Gap_Tracker) |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Supabase parallel write |
| `GAP_SUPPRESSION_FILE` | Phase 2 gap suppression JSON path |
| `ANTHROPIC_API_KEY` | Claude API |

---

## Phase 2 Hardening Checklist

- [x] pyproject.toml (build, ruff, mypy, pytest)
- [x] Type hints (hedis_gap_trail, cloud_status_badge, suppression_banner, hitl_admin_view)
- [x] Unit tests (tests/test_starguard_desktop.py)
- [x] CI workflow (.github/workflows/ci.yml)
- [x] ARCHITECTURE.md

---

## Phase 3 Forward Reference

**starguard-core** — Shared library extracting HEDIS_MEASURES, ROI calculators, compound framework from Desktop and Mobile. Reduces duplication and enables single-source updates. Deferred until Phase 2 gate closes.
