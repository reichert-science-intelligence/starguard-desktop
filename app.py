"""
StarGuard AI — HEDIS Portfolio Optimizer
Shiny for Python Application
© 2024–2026 Robert Reichert | StarGuard AI™
"""

from shiny import App, reactive, render, ui
from shiny.ui import tags
from htmltools import HTML
import pandas as pd

# ─── Import shared UI components ───
from modules.shared_ui import (
    page_header, metric_card, metrics_row, card, chart_container,
    controls, security_badge, tech_badges, qr_landing_card, footer,
    alert_info, alert_warning,
)

# ═══════════════════════════════════════════════════════════════
# SYNTHETIC DATA (fallback when database isn't connected)
# ═══════════════════════════════════════════════════════════════
PORTFOLIO_METRICS = {
    "roi": "33%", "star": "4.0", "members": "89,151", "compliance": "35.1%",
    "roi_delta": "+$1,264,020 annually", "star_delta": "+0.0 stars",
    "member_delta": "+ 37,511 eligible", "compliance_delta": "+2.3 pp vs prior",
}

MEASURES = [
    {"code": "BCS", "name": "Breast Cancer Screening", "compliance": 64.2, "gap": 8.1, "roi": 1.58},
    {"code": "COL", "name": "Colorectal Screening", "compliance": 58.7, "gap": 9.3, "roi": 1.50},
    {"code": "EED", "name": "Eye Exam for Diabetes", "compliance": 51.3, "gap": 7.2, "roi": 1.29},
    {"code": "HBD", "name": "HbA1c Control (<8%)", "compliance": 48.9, "gap": 6.8, "roi": 1.29},
    {"code": "CBP", "name": "Controlling Blood Pressure", "compliance": 56.1, "gap": 5.9, "roi": 1.37},
    {"code": "MAD", "name": "Med Adherence – Diabetes", "compliance": 72.4, "gap": 4.1, "roi": 1.50},
    {"code": "MAH", "name": "Med Adherence – HTN", "compliance": 74.8, "gap": 3.8, "roi": 1.50},
    {"code": "MAC", "name": "Med Adherence – Cholesterol", "compliance": 70.2, "gap": 4.5, "roi": 1.46},
    {"code": "SPC", "name": "Statin Use in CVD", "compliance": 66.9, "gap": 5.2, "roi": 1.52},
    {"code": "ABA", "name": "Adult BMI Assessment", "compliance": 82.1, "gap": 2.3, "roi": 1.60},
    {"code": "FRM", "name": "Fall Risk Management", "compliance": 44.3, "gap": 10.5, "roi": 1.28},
    {"code": "COA", "name": "Care for Older Adults", "compliance": 39.6, "gap": 12.8, "roi": 1.22},
]


# ═══════════════════════════════════════════════════════════════
# PAGE CONTENT FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def home_content():
    """Home dashboard page."""
    measures_df = pd.DataFrame(MEASURES)
    return ui.TagList(
        page_header(
            title="HEDIS Portfolio Optimizer",
            tagline="Intelligent HEDIS Portfolio Optimization",
            subtitle="Powered by Predictive Analytics & Machine Learning",
        ),
        security_badge(),
        tags.div(
            {"class": "sg-metrics-row"},
            metric_card("POTENTIAL ROI", PORTFOLIO_METRICS["roi"], PORTFOLIO_METRICS["roi_delta"], "positive"),
            metric_card("STAR RATING", PORTFOLIO_METRICS["star"], PORTFOLIO_METRICS["star_delta"], "neutral"),
            metric_card("MEMBERS", PORTFOLIO_METRICS["members"], PORTFOLIO_METRICS["member_delta"], "positive"),
            metric_card("COMPLIANCE", PORTFOLIO_METRICS["compliance"], PORTFOLIO_METRICS["compliance_delta"], "positive"),
        ),
        tags.div(
            {"class": "sg-metrics-row"},
            card("Portfolio Summary",
                tags.p(f"Tracking {len(MEASURES)} HEDIS measures"),
                tags.p("$5.4M value"),
            ),
            card("Optimization Priorities",
                tags.p("Top 3 gaps:"),
                tags.ul(
                    tags.li("COA: 12.8pt gap"),
                    tags.li("FRM: 10.5pt gap"),
                    tags.li("COL: 9.3pt gap"),
                ),
            ),
            card("Architecture Highlights",
                tags.p("Zero PHI exposure"),
                tags.p("HIPAA compliant"),
                tags.p("On-premises deployment"),
            ),
        ),
        # Bar chart rendered by server
        chart_container(
            tags.h3("HEDIS Measure Compliance Overview"),
            ui.output_ui("home_chart"),
        ),
        qr_landing_card(),
        footer(),
    )


def stub_page(title, icon, description):
    """Placeholder for pages not yet migrated."""
    return ui.TagList(
        page_header(title=title, tagline=f"{icon} {title}", subtitle=description),
        alert_info("This page is currently being migrated from Streamlit. Content coming soon!"),
        card("Migration Status",
            tags.p("The SQL queries and Plotly visualizations from the Streamlit version "
                    "will be ported to Shiny with minimal changes."),
            tags.p("The underlying data logic remains the same - only the UI framework changes."),
        ),
        footer(),
    )


def about_content():
    """About page with bio and QR code."""
    return ui.TagList(
        page_header(title="About StarGuard AI", tagline="Healthcare Data Science & AI Architecture"),
        card("Robert Reichert — Healthcare Data Scientist & AI Architect",
            tags.p("22+ years of experience across UPMC, Aetna, TriWest, BCBS, and Intel."),
            tags.p("Documented $148M+ in cost savings."),
            tags.p("Specializing in Medicare Advantage Star Ratings, HEDIS optimization, "
                    "and HIPAA-compliant AI systems."),
        ),
        qr_landing_card(),
        security_badge(),
        tech_badges(),
        footer(),
    )


def roi_by_measure_content():
    """ROI by Measure — full financial dashboard."""
    return ui.TagList(
        page_header(
            title="ROI by Measure",
            tagline="Measure-Level Return on Investment",
            subtitle="Financial performance across HEDIS quality measures",
        ),
        controls(
            ui.input_slider("roi_threshold", "Min ROI Threshold",
                            min=0.0, max=5.0, value=0.0, step=0.1),
            ui.input_slider("roi_success_rate", "Min Success Rate %",
                            min=0, max=100, value=0, step=5),
            ui.input_select("roi_plan_size", "Plan Size",
                            choices={"10000": "10K Members", "25000": "25K Members",
                                     "50000": "50K Members", "100000": "100K Members",
                                     "250000": "250K Members"},
                            selected="10000"),
        ),
        tags.div(
            {"class": "sg-metrics-row"},
            ui.output_ui("roi_kpi_investment"),
            ui.output_ui("roi_kpi_closures"),
            ui.output_ui("roi_kpi_revenue"),
            ui.output_ui("roi_kpi_net_benefit"),
        ),
        chart_container(
            tags.h3("ROI Performance by HEDIS Measure"),
            ui.output_ui("roi_main_chart"),
        ),
        tags.div(
            {"style": "display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;"},
            chart_container(
                tags.h3("Investment vs Revenue Impact"),
                ui.output_ui("roi_scatter_chart"),
            ),
            chart_container(
                tags.h3("Net Benefit by Measure"),
                ui.output_ui("roi_benefit_chart"),
            ),
        ),
        ui.navset_card_tab(
            ui.nav_panel("Financial Metrics", ui.output_data_frame("roi_financial_table")),
            ui.nav_panel("Performance Metrics", ui.output_data_frame("roi_performance_table")),
            ui.nav_panel("Complete Dataset", ui.output_data_frame("roi_complete_table")),
        ),
        tags.div(
            {"style": "margin: 1rem 0;"},
            ui.download_button("roi_download_csv", "📥 Export to CSV"),
        ),
        footer(),
    )


def cost_per_closure_content():
    """Cost Per Closure — intervention cost efficiency analysis."""
    return ui.TagList(
        page_header(
            title="Cost Per Closure",
            tagline="Intervention Cost Efficiency",
            subtitle="Cost analysis by outreach activity type",
        ),
        controls(
            ui.input_select("cost_activity_filter", "Activity Type",
                            choices={"all": "All Activities"},
                            selected="all"),
            ui.input_select("cost_plan_size", "Plan Size",
                            choices={"10000": "10K Members", "25000": "25K Members",
                                     "50000": "50K Members", "100000": "100K Members"},
                            selected="10000"),
        ),
        tags.div(
            {"class": "sg-metrics-row"},
            ui.output_ui("cost_kpi_avg"),
            ui.output_ui("cost_kpi_min"),
            ui.output_ui("cost_kpi_max"),
        ),
        chart_container(
            tags.h3("Cost Per Closure by Activity Type"),
            ui.output_ui("cost_scatter_chart"),
        ),
        tags.div(
            {"style": "display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;"},
            chart_container(
                tags.h3("Success Rate vs Cost"),
                ui.output_ui("cost_success_chart"),
            ),
            chart_container(
                tags.h3("Cost Efficiency Score"),
                ui.output_ui("cost_efficiency_chart"),
            ),
        ),
        ui.navset_card_tab(
            ui.nav_panel("Cost Analysis", ui.output_data_frame("cost_analysis_table")),
            ui.nav_panel("Efficiency Analysis", ui.output_data_frame("cost_efficiency_table")),
            ui.nav_panel("Complete Dataset", ui.output_data_frame("cost_complete_table")),
        ),
        tags.div(
            {"style": "margin: 1rem 0;"},
            ui.download_button("cost_download_csv", "📥 Export to CSV"),
        ),
        footer(),
    )


def star_rating_content():
    """Star Rating Impact — domain analysis and projections."""
    return ui.TagList(
        page_header(
            title="Star Rating Impact",
            tagline="CMS Star Rating Domain Analysis",
            subtitle="Current vs projected ratings by quality domain",
        ),
        tags.div(
            {"class": "sg-metrics-row"},
            ui.output_ui("star_kpi_current"),
            ui.output_ui("star_kpi_projected"),
            ui.output_ui("star_kpi_delta"),
            ui.output_ui("star_kpi_measures"),
        ),
        chart_container(
            tags.h3("Star Rating by Domain — Current vs Projected"),
            ui.output_ui("star_domain_chart"),
        ),
        chart_container(
            tags.h3("Measure Contribution to Star Rating"),
            ui.output_ui("star_contribution_chart"),
        ),
        ui.navset_card_tab(
            ui.nav_panel("Domain Summary", ui.output_data_frame("star_domain_table")),
            ui.nav_panel("Measure Detail", ui.output_data_frame("star_measure_table")),
        ),
        footer(),
    )


def compliance_trends_content():
    """Compliance Trends — historical trajectory analysis."""
    return ui.TagList(
        page_header(
            title="Compliance Trends",
            tagline="Historical Compliance Trajectory",
            subtitle="Monthly compliance rates across HEDIS measures",
        ),
        controls(
            ui.input_select("trend_measure", "Select Measure",
                            choices={"all": "All Measures", "BCS": "Breast Cancer Screening",
                                     "COL": "Colorectal Screening", "EED": "Diabetes Eye Exam",
                                     "CBP": "Blood Pressure Control", "MAD": "Med Adherence Diabetes",
                                     "MAH": "Med Adherence HTN", "HBD": "HbA1c Control"},
                            selected="all"),
            ui.input_select("trend_period", "Time Period",
                            choices={"6": "6 Months", "12": "12 Months", "24": "24 Months"},
                            selected="12"),
        ),
        tags.div(
            {"class": "sg-metrics-row"},
            ui.output_ui("trend_kpi_current"),
            ui.output_ui("trend_kpi_change"),
            ui.output_ui("trend_kpi_best"),
        ),
        chart_container(
            tags.h3("Compliance Rate Over Time"),
            ui.output_ui("trend_line_chart"),
        ),
        chart_container(
            tags.h3("Total Compliance Change Over Period"),
            ui.output_ui("trend_change_bars"),
        ),
        ui.navset_card_tab(
            ui.nav_panel("Monthly Data", ui.output_data_frame("trend_monthly_table")),
        ),
        footer(),
    )


# ═══════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION HTML
# ═══════════════════════════════════════════════════════════════
SIDEBAR_NAV_HTML = """
<div class="sg-nav-group-title">OVERVIEW</div>
<div class="sg-nav-link sg-nav-active" data-nav="home">🏠 Home</div>
<div class="sg-nav-link" data-nav="star_rating">⭐ Star Rating Impact</div>
<div class="sg-nav-link" data-nav="compliance">📈 Compliance Trends</div>

<div class="sg-nav-group-title">FINANCIAL ANALYSIS</div>
<div class="sg-nav-link" data-nav="roi_measure">💰 ROI by Measure</div>
<div class="sg-nav-link" data-nav="cost_closure">📉 Cost Per Closure</div>
<div class="sg-nav-link" data-nav="roi_calc">🧮 ROI Calculator</div>

<div class="sg-nav-group-title">CLINICAL ANALYTICS</div>
<div class="sg-nav-link" data-nav="gap">🔍 Gap Analysis</div>
<div class="sg-nav-link" data-nav="equity">🏥 Health Equity</div>
<div class="sg-nav-link" data-nav="intervention">📊 Intervention Perf.</div>
<div class="sg-nav-link" data-nav="measure_detail">🔬 Measure Detail</div>

<div class="sg-nav-group-title">INTELLIGENCE</div>
<div class="sg-nav-link" data-nav="ml">🤖 ML Predictions</div>
<div class="sg-nav-link" data-nav="risk">🎯 Member Risk</div>
<div class="sg-nav-link" data-nav="alerts">🔔 Alert Center</div>

<div class="sg-nav-group-title">OPERATIONS</div>
<div class="sg-nav-link" data-nav="optimizer">⚙️ Portfolio Optimizer</div>
<div class="sg-nav-link" data-nav="coordinator">👥 Coordinator Assign.</div>
<div class="sg-nav-link" data-nav="campaigns">📣 Campaign Mgmt.</div>
<div class="sg-nav-link" data-nav="plan_compare">📋 Plan Comparison</div>

<div class="sg-nav-group-title">SYSTEM</div>
<div class="sg-nav-link" data-nav="data_quality">✅ Data Quality</div>
<div class="sg-nav-link" data-nav="reporting">📄 Reporting</div>
<div class="sg-nav-link" data-nav="audit">📝 Audit Trail</div>
<div class="sg-nav-link" data-nav="settings">⚙️ Settings</div>
<div class="sg-nav-link" data-nav="about">ℹ️ About</div>
"""


# ═══════════════════════════════════════════════════════════════
# APP UI
# ═══════════════════════════════════════════════════════════════
app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.link(rel="stylesheet", href="styles.css"),
        ui.tags.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap",
        ),
        ui.tags.script(src="https://cdn.plot.ly/plotly-2.35.0.min.js"),
        ui.tags.script(src="nav.js"),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            tags.div(
                {"class": "sg-sidebar-brand"},
                tags.div({"class": "sg-star"}, "⭐"),
                tags.h2("StarGuard AI"),
                tags.p({"class": "sg-tagline"}, "HEDIS Portfolio Optimizer"),
            ),
            tags.hr(style="border-color: rgba(255,255,255,0.15); margin: 0.75rem 0;"),
            ui.HTML(SIDEBAR_NAV_HTML),
            width="260px",
            bg="#4A4468",
            open="always",
        ),
        # ─── Main content: navset_hidden with ALL pages ───
        ui.navset_hidden(
            ui.nav_panel("home", home_content()),
            ui.nav_panel("roi_measure", roi_by_measure_content()),
            ui.nav_panel("star_rating", star_rating_content()),
            ui.nav_panel("compliance", compliance_trends_content()),
            ui.nav_panel("cost_closure", cost_per_closure_content()),
            ui.nav_panel("roi_calc", stub_page("ROI Calculator", "🧮", "Interactive ROI modeling")),
            ui.nav_panel("gap", stub_page("Gap Analysis", "🔍", "Member-level gap identification")),
            ui.nav_panel("equity", stub_page("Health Equity", "🏥", "Equity-stratified performance")),
            ui.nav_panel("intervention", stub_page("Intervention Performance", "📊", "Campaign effectiveness")),
            ui.nav_panel("measure_detail", stub_page("Measure Detail", "🔬", "Deep-dive analytics")),
            ui.nav_panel("ml", stub_page("ML Predictions", "🤖", "Gap closure probability scoring")),
            ui.nav_panel("risk", stub_page("Member Risk Scoring", "🎯", "ML-driven risk stratification")),
            ui.nav_panel("alerts", stub_page("Alert Center", "🔔", "Real-time quality alerts")),
            ui.nav_panel("optimizer", stub_page("Portfolio Optimizer", "⚙️", "Resource allocation")),
            ui.nav_panel("coordinator", stub_page("Coordinator Assignment", "👥", "Workload distribution")),
            ui.nav_panel("campaigns", stub_page("Campaign Management", "📣", "Outreach planning")),
            ui.nav_panel("plan_compare", stub_page("Plan Comparison", "📋", "Plan benchmarking")),
            ui.nav_panel("data_quality", stub_page("Data Quality", "✅", "Data completeness monitoring")),
            ui.nav_panel("reporting", stub_page("Reporting & Export", "📄", "Report generation")),
            ui.nav_panel("audit", stub_page("Audit Trail", "📝", "Change tracking")),
            ui.nav_panel("settings", stub_page("Settings", "⚙️", "Configuration")),
            ui.nav_panel("about", about_content()),
            id="pages",
            selected="home",
        ),
    ),
)


# ═══════════════════════════════════════════════════════════════
# SERVER
# ═══════════════════════════════════════════════════════════════
def server(input, output, session):

    # ─── Navigation handler ───
    @reactive.effect
    @reactive.event(input.nav_target)
    def handle_nav():
        target = input.nav_target()
        print(f"SERVER NAV: switching to {target}")
        ui.update_navset("pages", selected=target)

    # ─── Home page chart ───
    @render.ui
    def home_chart():
        measures_df = pd.DataFrame(MEASURES)
        max_compliance = measures_df["compliance"].max()
        bars_html = ""
        for _, row in measures_df.iterrows():
            pct = (row["compliance"] / max_compliance) * 100
            color = "#10b981" if row["gap"] < 5 else "#F59E0B" if row["gap"] < 8 else "#ef4444"
            bars_html += f"""
            <div style="display:flex; align-items:center; margin:0.3rem 0; gap:0.5rem;">
                <span style="width:40px; font-size:0.78rem; font-weight:600; color:#4A4468;">{row['code']}</span>
                <div style="flex:1; background:#f3f4f6; border-radius:6px; height:22px; overflow:hidden;">
                    <div style="width:{pct:.0f}%; background:{color}; height:100%; border-radius:6px;
                                display:flex; align-items:center; justify-content:flex-end; padding-right:6px;">
                        <span style="font-size:0.72rem; color:#fff; font-weight:600;">{row['compliance']:.1f}%</span>
                    </div>
                </div>
            </div>"""
        return ui.HTML(bars_html)

    # ─── ROI by Measure: data loader ───
    @reactive.calc
    def roi_data():
        try:
            from utils.queries import get_roi_by_measure_query
            from data.db import query
            sql = get_roi_by_measure_query("2024-01-01", "2024-12-31")
            df = query(sql)
            if df.empty:
                raise ValueError("No data")
        except Exception:
            df = pd.DataFrame({
                "measure_code": ["BCS", "COL", "EED", "HBD", "CBP", "MAD",
                                 "MAH", "MAC", "SPC", "ABA", "FRM", "COA"],
                "measure_name": ["Breast Cancer Screening", "Colorectal Screening",
                    "Diabetes Eye Exam", "HbA1c Control", "Blood Pressure Control",
                    "Med Adherence Diabetes", "Med Adherence HTN",
                    "Med Adherence Cholesterol", "Statin Therapy",
                    "Adult BMI Assessment", "Fall Risk Management",
                    "Care for Older Adults"],
                "total_investment": [45000, 52000, 38000, 41000, 35000,
                    28000, 26000, 24000, 31000, 15000, 29000, 36000],
                "revenue_impact": [71000, 78000, 49000, 53000, 48000,
                    42000, 39000, 35000, 47000, 24000, 37000, 44000],
                "net_benefit": [26000, 26000, 11000, 12000, 13000,
                    14000, 13000, 11000, 16000, 9000, 8000, 8000],
                "roi_ratio": [1.58, 1.50, 1.29, 1.29, 1.37,
                    1.50, 1.50, 1.46, 1.52, 1.60, 1.28, 1.22],
                "successful_closures": [312, 289, 198, 215, 245,
                    356, 374, 328, 265, 412, 167, 192],
                "total_attempts": [501, 518, 412, 418, 414,
                    494, 503, 463, 399, 500, 374, 490],
                "success_rate": [62.3, 55.8, 48.1, 51.4, 59.2,
                    72.1, 74.3, 70.8, 66.5, 82.4, 44.7, 39.2],
            })

        # Calculate derived columns if missing
        if "net_benefit" not in df.columns:
            if "revenue_impact" in df.columns and "total_investment" in df.columns:
                df = df.copy()
                df["net_benefit"] = df["revenue_impact"] - df["total_investment"]

        # Apply filters
        threshold = input.roi_threshold()
        success_min = input.roi_success_rate()
        plan_size = int(input.roi_plan_size())
        scale = plan_size / 10000

        if threshold > 0:
            df = df[df["roi_ratio"] >= threshold].copy()
        if success_min > 0:
            df = df[df["success_rate"] >= success_min].copy()

        for col in ["total_investment", "revenue_impact", "net_benefit", "successful_closures"]:
            if col in df.columns:
                df[col] = (df[col] * scale).round(0)

        return df

    # ─── ROI KPI cards ───
    @render.ui
    def roi_kpi_investment():
        df = roi_data()
        val = df["total_investment"].sum()
        return metric_card("Total Investment", f"${val:,.0f}", "", "neutral")

    @render.ui
    def roi_kpi_closures():
        df = roi_data()
        val = df["successful_closures"].sum()
        return metric_card("Successful Closures", f"{val:,.0f}", "", "positive")

    @render.ui
    def roi_kpi_revenue():
        df = roi_data()
        val = df["revenue_impact"].sum()
        return metric_card("Revenue Impact", f"${val:,.0f}", "", "positive")

    @render.ui
    def roi_kpi_net_benefit():
        df = roi_data()
        if df.empty:
            val = 0
        else:
            # Calculate net benefit as revenue minus investment
            val = df["revenue_impact"].sum() - df["total_investment"].sum()
        delta_type = "positive" if val > 0 else "negative"
        return metric_card("Net Benefit", f"${val:,.0f}", "", delta_type)

    # ─── ROI Charts (Plotly as inline HTML) ───
    @render.ui
    def roi_main_chart():
        from utils.charts import create_bar_chart
        df = roi_data()
        fig = create_bar_chart(df, x_col="measure_code", y_col="roi_ratio",
                               title="ROI Ratio by HEDIS Measure")
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def roi_scatter_chart():
        from utils.charts import create_scatter_plot
        df = roi_data()
        fig = create_scatter_plot(df, x_col="total_investment", y_col="revenue_impact",
                                  title="Investment vs Revenue Impact")
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def roi_benefit_chart():
        from utils.charts import create_bar_chart
        df = roi_data()
        fig = create_bar_chart(df, x_col="measure_code", y_col="net_benefit",
                               title="Net Benefit by Measure", horizontal=True)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    # ─── ROI Data Tables ───
    @render.data_frame
    def roi_financial_table():
        df = roi_data()
        cols = ["measure_code", "measure_name", "total_investment",
                "revenue_impact", "net_benefit", "roi_ratio"]
        return render.DataGrid(df[[c for c in cols if c in df.columns]])

    @render.data_frame
    def roi_performance_table():
        df = roi_data()
        cols = ["measure_code", "measure_name", "successful_closures",
                "total_attempts", "success_rate"]
        return render.DataGrid(df[[c for c in cols if c in df.columns]])

    @render.data_frame
    def roi_complete_table():
        return render.DataGrid(roi_data())

    # ─── ROI CSV Export ───
    @render.download(filename="roi_by_measure.csv")
    async def roi_download_csv():
        yield roi_data().to_csv(index=False)

    # ═══════════════════════════════════════════════════════
    # COST PER CLOSURE PAGE
    # ═══════════════════════════════════════════════════════

    @reactive.calc
    def cost_data():
        try:
            from utils.queries import get_cost_per_closure_by_activity_query
            from data.db import query
            sql = get_cost_per_closure_by_activity_query("2024-01-01", "2024-12-31")
            df = query(sql)
            if df.empty:
                raise ValueError("No data")
        except Exception:
            df = pd.DataFrame({
                "activity_type": ["Phone Outreach", "Mail Campaign", "Home Visit",
                                  "Digital Outreach", "Provider Fax", "Care Coordination",
                                  "Text/SMS", "Email Campaign", "Community Event", "Telehealth"],
                "total_cost": [28500, 15200, 62000, 8900, 5400, 45000,
                               6200, 7800, 35000, 22000],
                "closures": [285, 95, 155, 178, 67, 225, 124, 89, 110, 165],
                "cost_per_closure": [100.0, 160.0, 400.0, 50.0, 80.6, 200.0,
                                     50.0, 87.6, 318.2, 133.3],
                "success_rate": [57.0, 38.0, 62.0, 71.2, 33.5, 67.5,
                                 62.0, 44.5, 55.0, 66.0],
                "efficiency_score": [82, 45, 35, 95, 55, 60, 90, 52, 40, 70],
            })

        # Calculate cost_per_closure if missing
        if "cost_per_closure" not in df.columns:
            if "total_cost" in df.columns and "closures" in df.columns:
                df = df.copy()
                df["cost_per_closure"] = (df["total_cost"] / df["closures"].replace(0, 1)).round(2)

        # Calculate efficiency_score if missing
        if "efficiency_score" not in df.columns:
            if "success_rate" in df.columns and "cost_per_closure" in df.columns:
                df = df.copy()
                max_cost = df["cost_per_closure"].max()
                df["efficiency_score"] = ((df["success_rate"] / 100) * (1 - df["cost_per_closure"] / max_cost) * 100).round(0)

        return df

    @render.ui
    def cost_kpi_avg():
        df = cost_data()
        val = df["cost_per_closure"].mean() if "cost_per_closure" in df.columns else 0
        return metric_card("Avg Cost/Closure", f"${val:,.0f}", "", "neutral")

    @render.ui
    def cost_kpi_min():
        df = cost_data()
        val = df["cost_per_closure"].min() if "cost_per_closure" in df.columns else 0
        return metric_card("Lowest Cost", f"${val:,.0f}", "", "positive")

    @render.ui
    def cost_kpi_max():
        df = cost_data()
        val = df["cost_per_closure"].max() if "cost_per_closure" in df.columns else 0
        return metric_card("Highest Cost", f"${val:,.0f}", "", "negative")

    @render.ui
    def cost_scatter_chart():
        from utils.charts import create_scatter_plot
        df = cost_data()
        x = "activity_type" if "activity_type" in df.columns else df.columns[0]
        y = "cost_per_closure" if "cost_per_closure" in df.columns else df.columns[1]
        fig = create_scatter_plot(df, x_col=x, y_col=y,
                                  title="Cost Per Closure by Activity")
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def cost_success_chart():
        from utils.charts import create_scatter_plot
        df = cost_data()
        x = "cost_per_closure" if "cost_per_closure" in df.columns else df.columns[0]
        y = "success_rate" if "success_rate" in df.columns else df.columns[1]
        fig = create_scatter_plot(df, x_col=x, y_col=y,
                                  title="Success Rate vs Cost Per Closure")
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def cost_efficiency_chart():
        from utils.charts import create_bar_chart
        df = cost_data()
        x = "activity_type" if "activity_type" in df.columns else df.columns[0]
        y = "efficiency_score" if "efficiency_score" in df.columns else df.columns[1]
        fig = create_bar_chart(df, x_col=x, y_col=y,
                               title="Cost Efficiency Score by Activity")
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.data_frame
    def cost_analysis_table():
        df = cost_data()
        cols = [c for c in ["activity_type", "total_cost", "closures", "cost_per_closure"]
                if c in df.columns]
        return render.DataGrid(df[cols] if cols else df)

    @render.data_frame
    def cost_efficiency_table():
        df = cost_data()
        cols = [c for c in ["activity_type", "success_rate", "efficiency_score", "cost_per_closure"]
                if c in df.columns]
        return render.DataGrid(df[cols] if cols else df)

    @render.data_frame
    def cost_complete_table():
        return render.DataGrid(cost_data())

    @render.download(filename="cost_per_closure.csv")
    async def cost_download_csv():
        yield cost_data().to_csv(index=False)

    # ═══════════════════════════════════════════════════════
    # STAR RATING IMPACT PAGE
    # ═══════════════════════════════════════════════════════

    @reactive.calc
    def star_data():
        return pd.DataFrame({
            "domain": ["Staying Healthy", "Managing Chronic Conditions",
                       "Member Experience", "Drug Safety & Accuracy",
                       "Complaints & Access", "Overall"],
            "current_rating": [3.5, 3.0, 4.0, 4.5, 3.5, 4.0],
            "projected_rating": [4.0, 3.5, 4.0, 4.5, 4.0, 4.5],
            "measure_count": [4, 3, 2, 1, 1, 1],
            "contribution_pct": [28, 22, 18, 12, 10, 10],
        })

    @render.ui
    def star_kpi_current():
        df = star_data()
        val = df.loc[df["domain"] == "Overall", "current_rating"].iloc[0]
        return metric_card("Current Rating", f"{val:.1f} ⭐", "", "neutral")

    @render.ui
    def star_kpi_projected():
        df = star_data()
        val = df.loc[df["domain"] == "Overall", "projected_rating"].iloc[0]
        return metric_card("Projected Rating", f"{val:.1f} ⭐", "", "positive")

    @render.ui
    def star_kpi_delta():
        df = star_data()
        row = df[df["domain"] == "Overall"].iloc[0]
        delta = row["projected_rating"] - row["current_rating"]
        sign = "+" if delta >= 0 else ""
        return metric_card("Rating Delta", f"{sign}{delta:.1f}", "", "positive" if delta > 0 else "neutral")

    @render.ui
    def star_kpi_measures():
        df = star_data()
        total = df["measure_count"].sum()
        return metric_card("Measures Tracked", str(total), "", "neutral")

    @render.ui
    def star_domain_chart():
        import plotly.graph_objects as go
        df = star_data()
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Current", x=df["domain"], y=df["current_rating"],
                             marker_color="#5B5B7E"))
        fig.add_trace(go.Bar(name="Projected", x=df["domain"], y=df["projected_rating"],
                             marker_color="#10b981"))
        fig.update_layout(barmode="group", title="Star Rating by Domain",
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#F5F3F9",
                          font=dict(family="Source Sans 3", color="#1f2937"),
                          yaxis=dict(range=[0, 5], dtick=1),
                          legend=dict(orientation="h", y=-0.15))
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def star_contribution_chart():
        import plotly.graph_objects as go
        df = star_data()
        df_sorted = df[df["domain"] != "Overall"].sort_values("contribution_pct", ascending=True)
        fig = go.Figure(go.Bar(
            x=df_sorted["contribution_pct"], y=df_sorted["domain"],
            orientation="h", marker_color="#6F5F96",
            text=df_sorted["contribution_pct"].apply(lambda v: f"{v}%"),
            textposition="outside"))
        fig.update_layout(title="Measure Contribution to Star Rating",
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#F5F3F9",
                          font=dict(family="Source Sans 3", color="#1f2937"),
                          xaxis=dict(title="Contribution %"))
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.data_frame
    def star_domain_table():
        return render.DataGrid(star_data())

    @render.data_frame
    def star_measure_table():
        df = pd.DataFrame(MEASURES)
        return render.DataGrid(df[["code", "name", "compliance", "gap", "roi"]])

    # ═══════════════════════════════════════════════════════
    # COMPLIANCE TRENDS PAGE
    # ═══════════════════════════════════════════════════════

    @reactive.calc
    def trend_data():
        import numpy as np
        np.random.seed(42)
        months = pd.date_range("2024-01-01", periods=12, freq="MS")
        measures = ["BCS", "COL", "EED", "CBP", "MAD", "MAH", "HBD"]
        base_rates = {"BCS": 58, "COL": 52, "EED": 46, "CBP": 50,
                      "MAD": 66, "MAH": 68, "HBD": 43}
        rows = []
        for m in measures:
            base = base_rates[m]
            for i, month in enumerate(months):
                rate = base + i * 0.8 + np.random.uniform(-1.5, 1.5)
                rows.append({"month": month, "measure_code": m,
                             "compliance_pct": round(rate, 1),
                             "target_pct": base + 15})
        df = pd.DataFrame(rows)

        # Apply measure filter
        selected = input.trend_measure()
        print(f"=== TREND MEASURE INPUT: '{selected}' (type: {type(selected).__name__}) ===")
        if selected != "all":
            df = df[df["measure_code"] == selected]
            print(f"=== FILTERED TO MEASURE: {selected}, ROWS AFTER FILTER: {len(df)} ===")

        # Apply period filter — keep last N months per measure
        period_months = int(input.trend_period())
        df = df.groupby("measure_code").tail(period_months).reset_index(drop=True)

        print(f"=== TREND DATA: {len(df)} rows, {df['measure_code'].nunique()} measures, {period_months} months ===")
        return df

    @render.ui
    def trend_kpi_current():
        df = trend_data()
        latest = df.groupby("measure_code")["compliance_pct"].last().mean()
        return metric_card("Current Avg", f"{latest:.1f}%", "", "neutral")

    @render.ui
    def trend_kpi_change():
        df = trend_data()
        by_measure = df.groupby("measure_code")["compliance_pct"]
        first_vals = by_measure.first().mean()
        last_vals = by_measure.last().mean()
        delta = last_vals - first_vals
        sign = "+" if delta >= 0 else ""
        return metric_card("Period Change", f"{sign}{delta:.1f} pp", "", "positive" if delta > 0 else "negative")

    @render.ui
    def trend_kpi_best():
        df = trend_data()
        best = df.groupby("measure_code")["compliance_pct"].last().idxmax()
        val = df.groupby("measure_code")["compliance_pct"].last().max()
        return metric_card("Top Performer", f"{best}: {val:.1f}%", "", "positive")

    @render.ui
    def trend_line_chart():
        print("=== TREND_LINE_CHART CALLED ===")
        import plotly.graph_objects as go
        df = trend_data()
        fig = go.Figure()
        colors = ["#5B5B7E", "#10b981", "#F59E0B", "#ef4444", "#6F5F96", "#8B7AB8", "#3D3159"]
        for i, measure in enumerate(df["measure_code"].unique()):
            mdf = df[df["measure_code"] == measure].sort_values("month")
            fig.add_trace(go.Scatter(
                x=mdf["month"], y=mdf["compliance_pct"],
                mode="lines+markers", name=measure,
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=5)))
        fig.update_layout(title="Compliance Trends by Measure",
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#F5F3F9",
                          font=dict(family="Source Sans 3", color="#1f2937"),
                          xaxis=dict(title="Month"),
                          yaxis=dict(title="Compliance %", range=[30, 85]),
                          legend=dict(orientation="h", y=-0.2),
                          height=400)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def trend_change_bars():
        print("=== TREND_CHANGE_BARS CALLED ===")
        df = trend_data()
        print(f"=== DATA ROWS: {len(df)}, MEASURES: {df['measure_code'].nunique() if 'measure_code' in df.columns else 'NO COL'} ===")
        measures = df["measure_code"].unique().tolist()
        deltas = []
        for m in measures:
            mdf = df[df["measure_code"] == m].sort_values("month")
            if len(mdf) >= 2:
                # Calculate change between MOST RECENT 2 months
                most_recent = mdf["compliance_pct"].iloc[-1]
                previous_month = mdf["compliance_pct"].iloc[-2]
                deltas.append(round(most_recent - previous_month, 1))
            else:
                deltas.append(0.0)

        max_abs = max(abs(d) for d in deltas) if deltas else 1
        bars_html = ""
        for measure, delta in sorted(zip(measures, deltas), key=lambda x: x[1], reverse=True):
            pct = abs(delta) / max_abs * 100
            color = "#10b981" if delta >= 0 else "#ef4444"
            sign = "+" if delta >= 0 else ""
            bars_html += f"""
            <div style="display:flex; align-items:center; margin:0.4rem 0; gap:0.5rem;">
                <span style="width:45px; font-size:0.82rem; font-weight:600; color:#4A4468;">{measure}</span>
                <div style="flex:1; background:#f3f4f6; border-radius:6px; height:26px; overflow:hidden; position:relative;">
                    <div style="width:{pct:.0f}%; background:{color}; height:100%; border-radius:6px;
                                display:flex; align-items:center; justify-content:flex-end; padding-right:8px;
                                min-width:50px;">
                        <span style="font-size:0.78rem; color:#fff; font-weight:600;">{sign}{delta:.1f} pp</span>
                    </div>
                </div>
            </div>"""
        print(f"=== BARS HTML LENGTH: {len(bars_html)} ===")
        return ui.HTML(bars_html)

    @render.data_frame
    def trend_monthly_table():
        df = trend_data()
        return render.DataGrid(df)


# ═══════════════════════════════════════════════════════════════
# CREATE APP
# ═══════════════════════════════════════════════════════════════
app = App(app_ui, server, static_assets=str(__import__("pathlib").Path(__file__).parent / "www"))
