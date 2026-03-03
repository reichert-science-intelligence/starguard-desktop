"""
Portfolio Optimization - What-If Scenarios
Phase 1 Week 2: Scenario modeling with ROI dashboard.
"""
from shiny import ui
from shinywidgets import output_widget
from modules.shared_ui import create_header, create_footer

PRIORITIZATION_CHOICES = {
    "cost_to_close": "Cost to Close",
    "highest_gap_count": "Highest Gap Count",
    "star_rating_impact": "Star Rating Impact",
    "disenrollment_risk": "Disenrollment Risk",
}


def portfolio_scenario_content():
    """UI for Portfolio What-If Scenarios."""
    return ui.TagList(
        create_header(),
        ui.card(
            ui.card_header("Portfolio Optimization - 'What-If' Scenarios"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.div(
                    ui.tags.label(
                        ui.tags.span("Members to Target: "),
                        ui.tags.span(
                            ui.output_text("scenario_target_members_display", inline=True),
                            style="color: #667eea; font-weight: 600;",
                        ),
                        style="display: block; margin-bottom: 8px; font-size: 0.95em;",
                    ),
                    ui.input_slider(
                        "scenario_target_members",
                        "",
                        min=100,
                        max=5000,
                        value=1000,
                        step=100,
                    ),
                ),
                ui.input_select(
                    "scenario_prioritization",
                    "Prioritization Strategy",
                    choices=PRIORITIZATION_CHOICES,
                ),
                ui.input_checkbox(
                    "scenario_include_sdoh",
                    "Include SDoH Interventions",
                    value=True,
                ),
                ui.input_action_button(
                    "scenario_run",
                    "Run Scenario",
                    class_="btn-primary",
                ),
                width=250,
            ),
            ui.div(
                output_widget("scenario_comparison"),
                ui.output_ui("scenario_summary"),
                ui.output_data_frame("scenario_top_targets"),
            ),
        ),
    ),
    create_footer(),
    )
