"""
Member Sentiment Analysis - CAHPS Risk Prediction
Phase 1 Week 1: Uses pre-computed sentiment scores from call transcript corpus.
"""
from shiny import ui
from shinywidgets import output_widget
from modules.shared_ui import create_header, create_footer

CAHPS_CHOICES = {
    "All": "All",
    "Getting Care Quickly": "Getting Care Quickly",
    "Customer Service": "Customer Service",
    "Care Coordination": "Care Coordination",
    "Health Plan Information": "Health Plan Information",
}


def sentiment_content():
    """UI for Member Sentiment Analysis - CAHPS Risk Prediction."""
    return ui.TagList(
        create_header(),
        ui.card(
            ui.card_header("Member Sentiment Analysis - CAHPS Risk Prediction"),
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select(
                    "sentiment_cahps_filter",
                    "CAHPS Category",
                    choices=CAHPS_CHOICES,
                ),
                ui.div(
                    ui.tags.label(
                        ui.tags.span("Risk Threshold: "),
                        ui.tags.span(
                            ui.output_text("sentiment_risk_threshold_display", inline=True),
                            style="color: #667eea; font-weight: 600;",
                        ),
                        style="display: block; margin-bottom: 8px; font-size: 0.95em;",
                    ),
                    ui.input_slider(
                        "sentiment_risk_threshold",
                        "",
                        min=-1.0,
                        max=0.0,
                        value=-0.4,
                        step=0.1,
                    ),
                ),
                ui.input_action_button(
                    "sentiment_analyze",
                    "Run Analysis",
                    class_="btn-primary",
                ),
                width=250,
            ),
            ui.div(
                output_widget("sentiment_distribution"),
                ui.output_data_frame("sentiment_high_risk_members"),
                ui.download_button("sentiment_high_risk_download", "Export High-Risk Members to CSV"),
                ui.output_ui("sentiment_intervention_recommendations"),
            ),
        ),
    ),
    create_footer(),
    )
