"""
StarGuard AI - Shared UI Components
Reusable UI components for the Shiny application
"""

from htmltools import tags, HTML, Tag
from shiny import ui


def sidebar_brand() -> Tag:
    """Sidebar brand section with logo and tagline"""
    return tags.div(
        tags.span("⭐", class_="sg-star"),
        tags.h2("StarGuard AI"),
        tags.p("HEDIS Portfolio Optimizer", class_="sg-tagline"),
        class_="sg-sidebar-brand"
    )


def nav_group_title(title: str) -> Tag:
    """Navigation group section header"""
    return tags.div(title, class_="sg-nav-group-title")


def page_header(title: str, tagline: str = "", subtitle: str = "") -> Tag:
    """Page header with purple gradient"""
    children = [
        tags.span("⭐", class_="sg-star"),
        tags.h1(title)
    ]
    
    if tagline:
        children.append(tags.p(tagline, class_="sg-header-tagline"))
    
    if subtitle:
        children.append(tags.p(subtitle, class_="sg-header-subtitle"))
    
    return tags.div(*children, class_="sg-header")


def metric_card(label: str, value: str, delta: str = "", delta_type: str = "positive") -> Tag:
    """Metric card component"""
    children = [
        tags.div(label, class_="sg-metric-label"),
        tags.div(value, class_="sg-metric-value")
    ]
    
    if delta:
        delta_class = f"sg-metric-delta {delta_type}"
        delta_symbol = "↑" if delta_type == "positive" else "↓" if delta_type == "negative" else ""
        children.append(tags.div(f"{delta_symbol} {delta}", class_=delta_class))
    
    return tags.div(*children, class_="sg-metric-card")


def metrics_row(*cards: Tag) -> Tag:
    """Row container for multiple metric cards"""
    return tags.div(*cards, class_="sg-metrics-row")


def card(title: str = None, *children) -> Tag:
    """Generic content card"""
    card_children = []
    
    if title:
        card_children.append(tags.h3(title, class_="sg-card-title"))
    
    card_children.extend(children)
    
    return tags.div(*card_children, class_="sg-card")


def chart_container(*children) -> Tag:
    """Container for Plotly charts"""
    return tags.div(*children, class_="sg-chart-container")


def controls(*children) -> Tag:
    """Filter panel container"""
    return tags.div(*children, class_="sg-controls")


def security_badge() -> Tag:
    """Security badge with HIPAA information"""
    return tags.div(
        tags.h4("🔒 Secure AI Architecture"),
        tags.p("Healthcare AI that sees everything, exposes nothing."),
        tags.div(
            tags.span("On-Premises", class_="sg-security-tag"),
            tags.span("Zero API Exposure", class_="sg-security-tag"),
            tags.span("HIPAA-First", class_="sg-security-tag")
        ),
        class_="sg-security-badge"
    )


def tech_badges() -> Tag:
    """Technology stack badges"""
    return tags.div(
        tags.span("🐍 Python"),
        tags.span("📊 Shiny"),
        tags.span("📈 Plotly"),
        tags.span("🐘 PostgreSQL"),
        tags.span("🤖 ML/AI"),
        class_="sg-tech-badges"
    )


def qr_landing_card() -> Tag:
    """QR code landing card"""
    return tags.div(
        tags.a(
            tags.img(src="qr-landing.png", alt="QR Code", class_="sg-qr-code"),
            href="https://tinyurl.com/bdevpdz5",
            target="_blank"
        ),
        tags.p("Scan for portfolio, resume & contact info", style="text-align: center; margin-top: 0.5rem; font-size: 0.85rem; color: #6b7280;"),
        class_="sg-card",
        style="max-width: 320px; margin: 0 auto; text-align: center;"
    )


def footer() -> Tag:
    """Footer with brand metrics"""
    return tags.div(
        tags.h2("⭐ HEDIS Portfolio Optimizer | StarGuard AI"),
        tags.p("Turning Data Into Stars"),
        tags.div(
            tags.div(
                tags.p("2.8–4.1×"),
                tags.p("ROI")
            ),
            tags.div(
                tags.p("$148M+"),
                tags.p("Savings")
            ),
            tags.div(
                tags.p("Zero"),
                tags.p("PHI Exposure")
            ),
            class_="sg-footer-metrics"
        ),
        tags.p("⚠️ Portfolio Demonstration: Using synthetic data to showcase real methodology and production-grade analytics.", style="font-size: 0.85rem; margin-top: 1rem; color: rgba(255,255,255,0.9);"),
        tags.p("© 2024–2026 Robert Reichert | StarGuard AI™", style="font-size: 0.85rem; margin-top: 1rem; color: rgba(255,255,255,0.8);"),
        class_="sg-footer"
    )


def alert_info(text: str) -> Tag:
    """Info alert box"""
    return tags.div(text, class_="sg-alert-info")


def alert_warning(text: str) -> Tag:
    """Warning alert box"""
    return tags.div(text, class_="sg-alert-warning")


def alert_success(text: str) -> Tag:
    """Success alert box"""
    return tags.div(text, class_="sg-alert-success")
