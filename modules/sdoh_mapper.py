"""
Social Determinants of Health - Barrier Analysis
Phase 1 Week 1: SDoH mapping and gap burden visualization.
"""
from shiny import ui
from shinywidgets import output_widget
from modules.shared_ui import create_header, create_footer


def sdoh_content():
    """UI for SDoH Barrier Analysis."""
    return ui.TagList(
        create_header(),
        ui.card(
            ui.card_header("Social Determinants of Health - Barrier Analysis"),
            output_widget("sdoh_heatmap"),
            ui.output_data_frame("sdoh_barrier_summary"),
        ),
        create_footer(),
    )
