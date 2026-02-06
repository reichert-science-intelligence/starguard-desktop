"""
StarGuard AI - HEDIS Portfolio Optimizer
Main Shiny Application
"""

from pathlib import Path
from htmltools import tags, HTML, Tag
from shiny import App, reactive, render, ui
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.shared_ui import (
    page_header, metric_card, metrics_row,
    card, chart_container, controls, security_badge, tech_badges, footer,
    alert_info, qr_landing_card
)

# ============================================================================
# SYNTHETIC DATA SECTION
# ============================================================================
# Placeholder data - will be replaced by real database queries later

PORTFOLIO_METRICS = {
    "potential_roi": "33%",
    "roi_delta": "+$1,264,020 annually",
    "star_rating": "4.0",
    "star_delta": "+0.0 stars",
    "members_optimized": "89,151",
    "members_delta": "37,514 closures",
    "compliance_rate": "35.1%",
    "compliance_delta": "+1.1%"
}

MEASURES = [
    {"name": "BCS", "compliance": 62.3, "target": 75.0, "gap": 12.7, "roi": 1.25},
    {"name": "COL", "compliance": 55.8, "target": 75.0, "gap": 19.2, "roi": 1.19},
    {"name": "EED", "compliance": 48.1, "target": 60.0, "gap": 11.9, "roi": 1.22},
    {"name": "HBD", "compliance": 51.4, "target": 70.0, "gap": 18.6, "roi": 1.18},
    {"name": "CBP", "compliance": 59.2, "target": 75.0, "gap": 15.8, "roi": 1.21},
    {"name": "MAD", "compliance": 72.1, "target": 80.0, "gap": 7.9, "roi": 1.28},
    {"name": "MAH", "compliance": 74.3, "target": 80.0, "gap": 5.7, "roi": 1.30},
    {"name": "MAC", "compliance": 70.8, "target": 80.0, "gap": 9.2, "roi": 1.26},
    {"name": "SPC", "compliance": 66.5, "target": 75.0, "gap": 8.5, "roi": 1.24},
    {"name": "ABA", "compliance": 82.4, "target": 85.0, "gap": 2.6, "roi": 1.35},
    {"name": "FRM", "compliance": 44.7, "target": 55.0, "gap": 10.3, "roi": 1.20},
    {"name": "COA", "compliance": 39.2, "target": 52.0, "gap": 12.8, "roi": 1.15}
]


# ============================================================================
# PAGE CONTENT FUNCTIONS
# ============================================================================

def home_content() -> Tag:
    """Home page content"""
    return tags.div(
        {"class": "sg-main"},
        page_header(
            "HEDIS Portfolio Optimizer",
            "Intelligent HEDIS Portfolio Optimization",
            "Powered by Predictive Analytics & Machine Learning"
        ),
        security_badge(),
        metrics_row(
            metric_card("Potential ROI", PORTFOLIO_METRICS["potential_roi"], PORTFOLIO_METRICS["roi_delta"], "positive"),
            metric_card("Star Rating", PORTFOLIO_METRICS["star_rating"], PORTFOLIO_METRICS["star_delta"], "neutral"),
            metric_card("Members Optimized", PORTFOLIO_METRICS["members_optimized"], PORTFOLIO_METRICS["members_delta"], "positive"),
            metric_card("Compliance Rate", PORTFOLIO_METRICS["compliance_rate"], PORTFOLIO_METRICS["compliance_delta"], "positive")
        ),
        tags.div(
            card(
                "Portfolio Summary",
                tags.p("Tracking 12 HEDIS measures"),
                tags.p(f"${5.4}M value"),
                tags.p(f"{PORTFOLIO_METRICS['members_optimized']} members")
            ),
            card(
                "Optimization Priorities",
                tags.p("Top 3 gaps:"),
                tags.ul(
                    tags.li("COA: 12.8pt gap"),
                    tags.li("EED: 11.9pt gap"),
                    tags.li("FRM: 10.3pt gap")
                )
            ),
            card(
                "Architecture Highlights",
                tags.p("Zero PHI exposure"),
                tags.p("HIPAA compliant"),
                tech_badges()
            ),
            qr_landing_card(),
            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 1.5rem 0;"
        ),
        chart_container(
            tags.h3("Compliance Gap by Measure"),
            ui.output_ui("home_chart", placeholder=True)
        ),
        footer()
    )


def stub_page(title: str, icon: str = "", description: str = "") -> Tag:
    """Stub page for pages not yet migrated"""
    tagline = f"{icon} {title}" if icon else title
    return tags.div(
        {"class": "sg-main"},
        page_header(title, tagline, description),
        alert_info("This page is currently being migrated from Streamlit. Content coming soon!"),
        card(
            "Migration Status",
            tags.p("The SQL queries and Plotly visualizations from the Streamlit version will be ported to Shiny with minimal changes."),
            tags.p("The underlying data logic remains the same - only the UI framework changes.")
        ),
        footer()
    )


def about_content() -> Tag:
    """About page content"""
    return tags.div(
        {"class": "sg-main"},
        page_header("About StarGuard AI", "Healthcare AI Architect", ""),
        card(
            "Robert Reichert",
            tags.p("22 years of healthcare analytics experience"),
            tags.p("$148M+ documented savings"),
            tags.p("Expertise: UPMC, Aetna, TriWest, BCBS, Intel"),
            tags.p("Specializations: HEDIS, Star Ratings, Health Equity, ML/AI")
        ),
        qr_landing_card(),
        security_badge(),
        footer()
    )


# ============================================================================
# APP UI
# ============================================================================

app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.link(rel="stylesheet", href="styles.css"),
        ui.tags.meta(name="viewport",
                     content="width=device-width, initial-scale=1.0, viewport-fit=cover"),
    ),

    ui.layout_sidebar(
        ui.sidebar(
            # Brand block
            tags.div(
                {"class": "sg-sidebar-brand"},
                tags.div({"class": "sg-star"}, "⭐"),
                tags.h2("StarGuard AI"),
                tags.p({"class": "sg-tagline"}, "HEDIS Portfolio Optimizer"),
            ),
            tags.hr(style="border-color: rgba(255,255,255,0.15); margin: 0.75rem 0;"),

            # Navigation using radio buttons styled as nav links
            tags.div({"class": "sg-nav-group-title"}, "OVERVIEW"),
            ui.input_radio_buttons(
                "nav", None,
                choices={
                    "home": "🏠 Home",
                    "star_rating": "⭐ Star Rating Impact",
                    "compliance": "📈 Compliance Trends",
                },
                selected="home",
            ),

            tags.div({"class": "sg-nav-group-title"}, "FINANCIAL ANALYSIS"),
            ui.input_radio_buttons(
                "nav_fin", None,
                choices={
                    "roi_measure": "💰 ROI by Measure",
                    "cost_closure": "📉 Cost Per Closure",
                    "roi_calc": "🧮 ROI Calculator",
                },
                selected=None,
            ),

            tags.div({"class": "sg-nav-group-title"}, "CLINICAL ANALYTICS"),
            ui.input_radio_buttons(
                "nav_clinical", None,
                choices={
                    "gap": "🔍 Gap Analysis",
                    "equity": "🏥 Health Equity",
                    "intervention": "📊 Intervention Perf.",
                    "measure_detail": "🔬 Measure Detail",
                },
                selected=None,
            ),

            tags.div({"class": "sg-nav-group-title"}, "INTELLIGENCE"),
            ui.input_radio_buttons(
                "nav_intel", None,
                choices={
                    "ml": "🤖 ML Predictions",
                    "risk": "🎯 Member Risk",
                    "alerts": "🔔 Alert Center",
                },
                selected=None,
            ),

            tags.div({"class": "sg-nav-group-title"}, "OPERATIONS"),
            ui.input_radio_buttons(
                "nav_ops", None,
                choices={
                    "optimizer": "⚙️ Portfolio Optimizer",
                    "coordinator": "👥 Coordinator Assign.",
                    "campaigns": "📣 Campaign Mgmt.",
                    "plan_compare": "📋 Plan Comparison",
                },
                selected=None,
            ),

            tags.div({"class": "sg-nav-group-title"}, "SYSTEM"),
            ui.input_radio_buttons(
                "nav_sys", None,
                choices={
                    "data_quality": "✅ Data Quality",
                    "reporting": "📄 Reporting",
                    "audit": "📝 Audit Trail",
                    "settings": "⚙️ Settings",
                    "about": "ℹ️ About",
                },
                selected=None,
            ),

            width="260px",
            bg="#4A4468",
            open="always",
        ),

        # Main content area — switches based on sidebar selection
        tags.div(
            {"class": "sg-main"},
            ui.output_ui("main_content"),
        ),
    ),
)


# ============================================================================
# SERVER FUNCTION
# ============================================================================

def server(input, output, session):
    """Server-side logic"""
    
    @reactive.calc
    def current_page():
        """Check all nav groups and return the active page key."""
        # Check each group — whichever was most recently clicked is active
        if input.nav() is not None:
            return input.nav()
        if input.nav_fin() is not None:
            return input.nav_fin()
        if input.nav_clinical() is not None:
            return input.nav_clinical()
        if input.nav_intel() is not None:
            return input.nav_intel()
        if input.nav_ops() is not None:
            return input.nav_ops()
        if input.nav_sys() is not None:
            return input.nav_sys()
        return "home"

    @output
    @render.ui
    def main_content():
        page = current_page()
        pages = {
            "home": home_content,
            "star_rating": lambda: stub_page("Star Rating Impact", "⭐", "Star rating projections"),
            "compliance": lambda: stub_page("Compliance Trends", "📈", "Historical compliance trajectory"),
            "roi_measure": lambda: stub_page("ROI by Measure", "💰", "Measure-level ROI analysis"),
            "cost_closure": lambda: stub_page("Cost Per Closure", "📉", "Intervention cost efficiency"),
            "roi_calc": lambda: stub_page("ROI Calculator", "🧮", "Interactive ROI modeling"),
            "gap": lambda: stub_page("Gap Analysis", "🔍", "Member-level gap identification"),
            "equity": lambda: stub_page("Health Equity", "🏥", "Equity-stratified performance"),
            "intervention": lambda: stub_page("Intervention Performance", "📊", "Campaign effectiveness"),
            "measure_detail": lambda: stub_page("Measure Detail", "🔬", "Deep-dive analytics"),
            "ml": lambda: stub_page("ML Predictions", "🤖", "Gap closure probability scoring"),
            "risk": lambda: stub_page("Member Risk Scoring", "🎯", "ML-driven risk stratification"),
            "alerts": lambda: stub_page("Alert Center", "🔔", "Real-time quality alerts"),
            "optimizer": lambda: stub_page("Portfolio Optimizer", "⚙️", "Resource allocation"),
            "coordinator": lambda: stub_page("Coordinator Assignment", "👥", "Workload distribution"),
            "campaigns": lambda: stub_page("Campaign Management", "📣", "Outreach planning"),
            "plan_compare": lambda: stub_page("Plan Comparison", "📋", "Plan benchmarking"),
            "data_quality": lambda: stub_page("Data Quality", "✅", "Data completeness monitoring"),
            "reporting": lambda: stub_page("Reporting & Export", "📄", "Report generation"),
            "audit": lambda: stub_page("Audit Trail", "📝", "Change tracking"),
            "settings": lambda: stub_page("Settings", "⚙️", "Configuration"),
            "about": about_content,
        }
        builder = pages.get(page, home_content)
        return builder() if callable(builder) else builder
    
    @output
    @render.ui
    def home_chart():
        """Home page compliance chart"""
        chart_html = tags.div(
            style="display: flex; flex-direction: column; gap: 0.5rem;"
        )
        
        for measure in MEASURES:
            gap = measure["gap"]
            compliance = measure["compliance"]
            
            # Determine bar color based on gap
            if gap < 8:
                bar_color = "var(--sg-green)"
            elif gap < 10:
                bar_color = "var(--sg-gold)"
            else:
                bar_color = "var(--sg-red)"
            
            bar_width = f"{compliance}%"
            
            measure_row = tags.div(
                tags.span(measure["name"], style=f"display: inline-block; width: 200px; text-align: left; font-weight: 600;"),
                tags.div(
                    tags.div(
                        style=f"background: {bar_color}; height: 24px; width: {bar_width}; border-radius: 4px; display: inline-block;"
                    ),
                    tags.span(f"{compliance:.1f}%", style="margin-left: 8px; font-weight: 600;"),
                    tags.span(f"(Gap: {gap:.1f}pt)", style="margin-left: 8px; color: #6b7280; font-size: 0.9rem;")
                ),
                style="display: flex; align-items: center; gap: 1rem; margin: 0.5rem 0; padding: 0.5rem; background: #f9fafb; border-radius: 4px;"
            )
            
            chart_html.children.append(measure_row)
        
        return chart_html


# ============================================================================
# APP OBJECT
# ============================================================================

app = App(
    app_ui,
    server,
    static_assets=str(Path(__file__).parent / "www")
)
