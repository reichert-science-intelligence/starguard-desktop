# Shiny Demo Status — What's Working vs Placeholders

## Quick diagnosis (as of this audit)

### Backend files in `starguard-shiny/`

| File | Exists | Notes |
|------|--------|--------|
| `utils/intervention_analysis.py` | ✅ | Portfolio optimization (3 strategies). |
| `utils/queries.py` | ✅ | ROI by measure, cost, etc. |
| `utils/charts.py`, `data_helpers.py`, `plan_context.py`, `enhanced_charts.py` | ✅ | Used by ROI/Cost/Star pages. |
| `utils/roi_calculator.py` | ❌ → ✅ | **Added:** 3-method ROI + recommend (slim, no DB). |
| `utils/measure_analysis.py` | ❌ → ✅ | **Added:** gap analysis + validated (slim). |
| `utils/validation_badges.py` | ❌ | In phase4_dashboard only; optional for Shiny. |
| `compound_framework/financial_impact.py` | ✅ | Financial calculations. |
| `compound_framework/ai_engine_enhanced.py` | ✅ | Used by HEDIS Calculator. |

### Pages: working vs placeholder

| Page | Status | Notes |
|------|--------|--------|
| **Home** | ✅ WORKING | Metrics, chart, cards. |
| **ROI by Measure** | ✅ WORKING | Tables, charts, filters. |
| **Star Rating** | ✅ WORKING | Domain summary, measure detail. |
| **Compliance Trends** | ✅ WORKING | Compliance data. |
| **Cost Per Closure** | ✅ WORKING | Cost analysis, charts. |
| **Self-Correcting HEDIS Calculator** | ✅ WORKING | Forms, results, SQL, compound framework. |
| **Intervention Portfolio Optimizer** | ✅ WORKING | Budget input, 3 strategy tabs, intervention table. |
| **ROI Calculator** (3 methods) | ❌ → ✅ | **Wired:** inputs + 3-method comparison + recommendation. |
| **Gap Analysis** (validated) | ❌ → ✅ | **Wired:** measure select + validated gap + confidence. |
| **About** | ✅ WORKING | Bio, QR, badges. |
| Health Equity, Intervention Performance, Measure Detail, ML, Risk, Alerts, etc. | ⏳ PLACEHOLDER | Still show "being migrated" message. |

---

## P0 for Saturday demo (must-have)

1. **Self-Correcting HEDIS Calculator** — ✅ Working.
2. **Gap Analysis** — ✅ Wired (validated content + confidence).
3. **ROI Calculator** — ✅ Wired (3 methods + recommendation).
4. **Intervention Portfolio Optimizer** — ✅ Working.

---

## Verification commands

```bash
cd starguard-shiny
ls -la utils/
ls -la compound_framework/
shiny run app.py
```

Then in the app:

- **ROI Calculator:** Sidebar → ROI Calculator. Set investment, closures, revenue; see "Compare ROI Methods" table and recommendation.
- **Gap Analysis:** Sidebar → Gap Analysis. Select measure; see validated gap metrics, confidence, timeline.
- **Portfolio Optimizer:** Sidebar → Portfolio Optimizer. Set budget; switch tabs (Max Star / Max ROI / Balanced); see intervention details table.

---

## If short on time

- **Option A:** Demo only the working + newly wired pages (HEDIS Calc, Gap, ROI Calc, Portfolio Optimizer, Home, ROI by Measure, Cost Per Closure).
- **Option B:** Use Streamlit for full feature set; position Shiny as "production migration in progress."
- **Option C:** Leave remaining nav items as "Phase 2" and focus demo on the four P0 pages above.
