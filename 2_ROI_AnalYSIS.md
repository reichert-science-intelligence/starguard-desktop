# Phase 2: ROI Analysis Pages Migration Plan

## Overview
This document analyzes the ROI-related pages from the Streamlit app to plan their migration to Shiny for Python.

## ROI Pages Identified

### 1. ROI by Measure (`1_📊_ROI_by_Measure.py`)
**Status:** Tier 1 Priority - Core Financial Dashboard

**Key Features:**
- Bar chart showing ROI performance across all HEDIS measures
- KPI metrics: Total Investment, Successful Closures, Revenue Impact, Net Benefit
- Multiple visualization views:
  - Investment vs Revenue Impact (Scatter)
  - Success Rate by Measure (Bar)
  - Net Benefit by Measure (Grouped Bar)
  - Multi-Dimensional Radar Chart (Top 5 measures)
- Tabbed data tables: Financial Metrics, Performance Metrics, ROI Analysis, Complete Dataset
- CSV export functionality
- Sidebar filters: ROI threshold, Success rate, Investment range
- Membership size scaling (10K baseline, scales to plan size)

**Dependencies:**
- `utils.database.execute_query`
- `utils.queries.get_roi_by_measure_query`
- `utils.charts.create_bar_chart`, `create_scatter_plot`, `create_grouped_bar_chart`
- `utils.enhanced_charts.create_wow_radar_chart`
- `utils.data_helpers.show_data_availability_warning`, `get_data_date_range`, `format_date_display`
- `utils.plan_context.get_plan_context`, `get_plan_size_scenarios`
- `src.ui.compact_components.compact_metric_card`, `compact_insight_box`
- `utils.standard_sidebar.render_standard_sidebar`

**Shiny Migration Strategy:**
1. Create `pages/roi_by_measure.py` module
2. Use `ui.layout_sidebar` for filters (already in place)
3. Use `plotly` for charts (already available)
4. Use `ui.navset_tab` for tabbed data views
5. Use `ui.download_button` for CSV export
6. Reuse `data.db.query` for database access
7. Create `utils/charts.py` with Shiny-compatible chart functions

---

### 2. Cost Per Closure (`2_💰_Cost_Per_Closure.py`)
**Status:** Tier 1 Priority - Cost Efficiency Analysis

**Key Features:**
- Scatter plot: Cost per closure by activity type
- Additional views:
  - Success Rate vs Cost Per Closure (Scatter)
  - Activity Usage Frequency (Bar)
  - Cost Efficiency Score (Bar)
- Tabbed data tables: Cost Analysis, Performance Analysis, Efficiency Analysis, Complete Dataset
- Summary metrics: Average/Min/Max Cost per Closure
- CSV export functionality
- Sidebar filters: Date range, Membership size

**Dependencies:**
- `utils.database.execute_query`
- `utils.queries.get_cost_per_closure_by_activity_query`
- `utils.charts.create_scatter_plot`, `create_bar_chart`
- `utils.data_helpers.show_data_availability_warning`, `get_data_date_range`, `format_date_display`
- `utils.plan_context.get_plan_size_scenarios`
- `utils.data_validation.ensure_no_zero_data`

**Shiny Migration Strategy:**
1. Create `pages/cost_per_closure.py` module
2. Use `plotly.graph_objects.Scatter` for scatter plots
3. Use `ui.navset_tab` for tabbed views
4. Use `ui.value_box` for summary metrics
5. Reuse database and chart utilities

---

### 3. ROI Calculator (`11_💰_ROI_Calculator.py`)
**Status:** Tier 2 Priority - Interactive Calculator

**Key Features:**
- Interactive ROI calculation with user inputs:
  - Investment Amount
  - Expected Closures
  - Revenue per Closure
- Real-time ROI calculation and display
- Visualizations:
  - ROI Breakdown (Bar chart)
  - Sensitivity Analysis (Scatter with trendline)
  - Portfolio Comparison (Bar chart)
  - Investment vs Return Distribution (Pie chart)
- Sidebar filters: Target ROI, Investment range, Success rate assumption
- Comparison with portfolio average ROI

**Dependencies:**
- `utils.database.execute_query`
- `utils.queries.get_roi_by_measure_query`, `get_portfolio_summary_query`
- `utils.enhanced_charts.create_wow_bar_chart`, `create_wow_scatter`, `create_wow_pie_chart`
- `utils.roi_calculator.ROICalculator` (complex calculation logic)
- `utils.data_helpers.show_data_availability_warning`, `get_data_date_range`, `format_date_display`

**Shiny Migration Strategy:**
1. Create `pages/roi_calculator.py` module
2. Use `ui.input_number` for user inputs
3. Use `@reactive.calc` for real-time ROI calculations
4. Use `@render.plotly` for dynamic chart updates
5. Port `ROICalculator` class to Shiny-compatible module
6. Use `ui.value_box` for summary metrics

---

## Common Patterns Identified

### 1. Database Queries
**Streamlit Pattern:**
```python
from utils.database import execute_query
from utils.queries import get_roi_by_measure_query

query = get_roi_by_measure_query(start_date, end_date)
df = execute_query(query)
```

**Shiny Equivalent:**
```python
from data.db import query
from utils.queries import get_roi_by_measure_query

@reactive.calc
def roi_data():
    sql = get_roi_by_measure_query(start_date(), end_date())
    return query(sql)
```

### 2. Chart Rendering
**Streamlit Pattern:**
```python
from utils.charts import create_bar_chart
fig = create_bar_chart(df, x_col="measure_code", y_col="roi_ratio", ...)
st.plotly_chart(fig, use_container_width=True)
```

**Shiny Equivalent:**
```python
from utils.charts import create_bar_chart

@output
@render.plotly
def roi_chart():
    df = roi_data()
    return create_bar_chart(df, x_col="measure_code", y_col="roi_ratio", ...)
```

### 3. Sidebar Filters
**Streamlit Pattern:**
```python
from utils.standard_sidebar import render_standard_sidebar, get_sidebar_date_range

render_standard_sidebar(...)
start_date, end_date = get_sidebar_date_range()
```

**Shiny Equivalent:**
```python
# Filters already in sidebar via ui.input_radio_buttons
# Use reactive inputs directly
start_date = input.start_date()
end_date = input.end_date()
```

### 4. Tabbed Data Views
**Streamlit Pattern:**
```python
selected_tab = st.radio("Select View", ["Financial", "Performance", ...], horizontal=True)
if selected_tab == "Financial":
    st.dataframe(financial_df)
```

**Shiny Equivalent:**
```python
ui.navset_tab(
    ui.nav_panel("Financial", ui.output_data_frame("financial_table")),
    ui.nav_panel("Performance", ui.output_data_frame("performance_table")),
)
```

### 5. CSV Export
**Streamlit Pattern:**
```python
csv = df.to_csv(index=False)
st.download_button("Download CSV", data=csv, file_name="...", mime="text/csv")
```

**Shiny Equivalent:**
```python
@output
@render.download(filename="roi_data.csv")
def download_csv():
    df = roi_data()
    return df.to_csv(index=False)
```

---

## Migration Priority

### Phase 2A: Core ROI Dashboard (Week 1)
1. ✅ **ROI by Measure** - Most important financial view
   - Estimated effort: 4-6 hours
   - Dependencies: Chart utilities, query functions

### Phase 2B: Cost Analysis (Week 1-2)
2. ✅ **Cost Per Closure** - Cost efficiency analysis
   - Estimated effort: 3-4 hours
   - Dependencies: Scatter plot utilities

### Phase 2C: Interactive Tools (Week 2)
3. ⚠️ **ROI Calculator** - More complex, requires reactive calculations
   - Estimated effort: 6-8 hours
   - Dependencies: ROI calculation logic, enhanced charts

---

## Required Utilities to Port

### 1. Chart Functions (`utils/charts.py`)
- `create_bar_chart(df, x_col, y_col, title, ...)`
- `create_scatter_plot(df, x_col, y_col, size_col, color_col, ...)`
- `create_grouped_bar_chart(df, x_col, y_cols, ...)`

**Shiny Implementation:**
- Use `plotly.graph_objects` directly
- Return `go.Figure` objects
- Compatible with `@render.plotly`

### 2. Enhanced Charts (`utils/enhanced_charts.py`)
- `create_wow_radar_chart(df, categories, group_col, ...)`
- `create_wow_bar_chart(df, x_col, y_col, ...)`
- `create_wow_scatter(df, x_col, y_col, ...)`
- `create_wow_pie_chart(df, values_col, names_col, ...)`

**Shiny Implementation:**
- Port color palettes and styling
- Use `plotly.graph_objects` with custom templates

### 3. Query Functions (`utils/queries.py`)
- `get_roi_by_measure_query(start_date, end_date)`
- `get_cost_per_closure_by_activity_query(start_date, end_date)`
- `get_portfolio_summary_query(start_date, end_date)`

**Shiny Implementation:**
- Keep as-is (pure SQL string functions)
- No changes needed

### 4. Data Helpers (`utils/data_helpers.py`)
- `show_data_availability_warning(start_date, end_date)`
- `get_data_date_range()`
- `format_date_display(date)`

**Shiny Implementation:**
- Convert `st.warning()` to `ui.Notification`
- Convert `st.info()` to `ui.tags.div` with info styling
- Date formatting functions unchanged

### 5. ROI Calculator (`utils/roi_calculator.py`)
- `ROICalculator` class with complex calculation logic
- Confidence intervals, sensitivity analysis

**Shiny Implementation:**
- Port class as-is
- Use `@reactive.calc` for calculations
- Return dictionaries for display

---

## File Structure for Shiny Migration

```
starguard-shiny/
├── app.py                    # Main app (already done)
├── modules/
│   └── shared_ui.py          # Shared UI components (already done)
├── pages/
│   ├── roi_by_measure.py     # NEW: ROI by Measure page
│   ├── cost_per_closure.py   # NEW: Cost Per Closure page
│   └── roi_calculator.py     # NEW: ROI Calculator page
├── utils/
│   ├── charts.py             # NEW: Chart creation functions
│   ├── enhanced_charts.py    # NEW: Enhanced chart functions
│   ├── queries.py            # NEW: SQL query builders
│   ├── data_helpers.py       # NEW: Data utility functions
│   └── roi_calculator.py     # NEW: ROI calculation logic
└── data/
    └── db.py                 # Database connection (already done)
```

---

## Testing Checklist

### ROI by Measure
- [ ] Data loads correctly from database
- [ ] Charts render with correct data
- [ ] Filters update results
- [ ] Tabbed views switch correctly
- [ ] CSV export works
- [ ] Membership scaling works
- [ ] Mobile responsive

### Cost Per Closure
- [ ] Scatter plot renders correctly
- [ ] Additional views display properly
- [ ] Summary metrics calculate correctly
- [ ] CSV export works
- [ ] Mobile responsive

### ROI Calculator
- [ ] Inputs update calculations in real-time
- [ ] Charts update when inputs change
- [ ] Portfolio comparison works
- [ ] Sensitivity analysis displays correctly
- [ ] Mobile responsive

---

## Next Steps

1. **Create utility modules** (`utils/charts.py`, `utils/queries.py`, etc.)
2. **Port ROI by Measure page** (highest priority)
3. **Port Cost Per Closure page**
4. **Port ROI Calculator page**
5. **Test all pages** with real database data
6. **Update navigation** in `app.py` to link to new pages

---

## Notes

- All pages use extensive CSS styling (already in `www/styles.css`)
- Database connection already working (`data/db.py`)
- Plotly charts are framework-agnostic (work in both Streamlit and Shiny)
- Main challenge: Converting Streamlit's reactive model to Shiny's reactive model
- Sidebar navigation already implemented in `app.py`
