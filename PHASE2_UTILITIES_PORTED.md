# Phase 2: Utility Modules Ported

## Summary
All shared utility modules have been successfully ported from Streamlit to Shiny. These modules provide the foundation for ROI page migrations.

---

## Files Copied and Modified

### ✅ STEP 1: `utils/queries.py`
**Status:** Copied as-is (no changes needed)

**Functions:**
- `get_roi_by_measure_query(start_date, end_date)` - Returns SQL string
- `get_cost_per_closure_by_activity_query(start_date, end_date, min_uses)` - Returns SQL string
- `get_monthly_intervention_trend_query(start_date, end_date)` - Returns SQL string
- `get_budget_variance_by_measure_query(start_date, end_date)` - Returns SQL string
- `get_cost_tier_comparison_query(start_date, end_date)` - Returns SQL string
- `get_portfolio_summary_query(start_date, end_date)` - Returns SQL string

**Modifications:** None - pure SQL string builders work identically in both frameworks

---

### ✅ STEP 2: `utils/charts.py`
**Status:** Copied and updated with StarGuard theme

**Functions:**
- `create_bar_chart(df, x_col, y_col, title, ...)` - Returns `go.Figure`
- `create_scatter_plot(df, x_col, y_col, size_col, color_col, ...)` - Returns `go.Figure`
- `create_line_chart(df, x_col, y_cols, title, ...)` - Returns `go.Figure`
- `create_waterfall_chart(df, measure_col, budget_col, ...)` - Returns `go.Figure`
- `create_grouped_bar_chart(df, x_col, y_cols, title, ...)` - Returns `go.Figure`
- `format_column_label(column_name)` - Returns formatted label string

**Modifications:**
1. ✅ Removed `desktop_visualizations` import (not needed for Shiny)
2. ✅ Updated `MEDICAL_THEME` colors to StarGuard theme:
   - Primary: `#5B5B7E` (was `#4e2a84`)
   - Secondary: `#6F5F96` (was `#8f67d1`)
   - Accent: `#8B7AB8` (was `#2d7d32`)
   - Success: `#10b981` (was `#388e3c`)
   - Warning: `#F59E0B` (was `#f57c00`)
   - Background: `#F5F3F9` (was `#f8f9fa`)
   - Text: `#1f2937` (was `#212529`)
3. ✅ Updated font family: `"Source Sans 3, sans-serif"` (was `"Arial, sans-serif"`)
4. ✅ Updated background colors:
   - `plot_bgcolor`: `#FFFFFF` (was `"white"`)
   - `paper_bgcolor`: `#F5F3F9` (was `"white"`)

---

### ✅ STEP 3: `utils/enhanced_charts.py`
**Status:** Copied and updated with StarGuard theme

**Functions:**
- `create_wow_scatter(df, x_col, y_col, ...)` - Returns `go.Figure`
- `create_wow_bar_chart(df, x_col, y_col, ...)` - Returns `go.Figure`
- `create_wow_line_chart(df, x_col, y_cols, ...)` - Returns `go.Figure`
- `create_wow_pie_chart(df, values_col, names_col, ...)` - Returns `go.Figure`
- `create_wow_heatmap(df, x_col, y_col, values_col, ...)` - Returns `go.Figure`
- `create_wow_area_chart(df, x_col, y_cols, ...)` - Returns `go.Figure`
- `create_wow_radar_chart(df, categories, values, group_col, ...)` - Returns `go.Figure`

**Modifications:**
1. ✅ Updated `COLOR_PALETTES["medical"]` to StarGuard colors:
   - `["#5B5B7E", "#6F5F96", "#8B7AB8", "#10b981", "#F59E0B", ...]`
2. ✅ Updated `RADAR_COLORS["medical"]` to StarGuard colors
3. ✅ Updated background colors:
   - `plot_bgcolor`: `#FFFFFF`
   - `paper_bgcolor`: `#F5F3F9`
4. ✅ Updated font family: `"Source Sans 3, sans-serif"` (was `"Arial Black"`)

---

### ✅ STEP 4: `utils/data_helpers.py`
**Status:** Copied and adapted for Shiny

**Functions:**
- `format_date_display(date)` - Returns formatted date string (unchanged)
- `format_month_display(month_str)` - Returns formatted month string (unchanged)
- `get_data_date_range()` - Returns `(min_date, max_date)` tuple (updated to use `data.db.query`)
- `show_data_availability_warning(selected_start, selected_end)` - Returns `Dict[str, str]` or `None` (was `st.warning()`)

**Modifications:**
1. ✅ Removed `streamlit` import
2. ✅ Updated `get_data_date_range()` to use `data.db.query()` instead of `get_connection()`
3. ✅ Changed `show_data_availability_warning()` to return dict instead of calling `st.warning()`:
   - Returns: `{"type": "warning", "text": "message"}` or `None`
   - Shiny pages will use this dict to display warnings via `ui.Notification` or `ui.tags.div`

---

### ✅ STEP 5: `utils/plan_context.py`
**Status:** Copied and updated database import

**Functions:**
- `get_plan_context()` - Returns plan context dict (updated to use `data.db.query`)
- `get_plan_size_scenarios()` - Returns plan size scenarios dict (unchanged)
- `get_industry_benchmarks()` - Returns benchmark data dict (unchanged)

**Modifications:**
1. ✅ Updated `get_plan_context()` to use `data.db.query()` instead of `utils.database.execute_query`
2. ✅ All calculation functions unchanged (pure Python)

---

### ✅ STEP 6: `utils/__init__.py`
**Status:** Created

**Content:**
```python
# StarGuard AI utilities
```

---

## Import Test Results

✅ **All imports successful:**
```python
from utils.queries import get_roi_by_measure_query
from utils.charts import create_bar_chart
from utils.data_helpers import get_data_date_range
from utils.enhanced_charts import create_wow_radar_chart
from utils.plan_context import get_plan_context
```

**Result:** `All utility modules imported successfully`

---

## Summary of Changes

| File | Changes Made |
|------|-------------|
| `queries.py` | None - copied as-is |
| `charts.py` | Updated colors, font, backgrounds (StarGuard theme) |
| `enhanced_charts.py` | Updated colors, font, backgrounds (StarGuard theme) |
| `data_helpers.py` | Removed Streamlit calls, updated database import |
| `plan_context.py` | Updated database import |
| `__init__.py` | Created new file |

---

## Next Steps

Ready to proceed with Phase 2B: Port ROI pages
1. Port `pages/roi_by_measure.py`
2. Port `pages/cost_per_closure.py`
3. Port `pages/roi_calculator.py`

All utility dependencies are now available and tested.
