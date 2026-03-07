"""
Outreach Channel Optimization
Phase 1 Week 1: Channel effectiveness and campaign recommendations.
"""

from shiny import ui
from shinywidgets import output_widget

from modules.shared_ui import create_footer, create_header


def channel_optimizer_content():
    """UI for Outreach Channel Optimization."""
    return ui.TagList(
        create_header(),
        ui.card(
            ui.card_header("Outreach Channel Optimization"),
            output_widget("channel_effectiveness"),
            ui.output_data_frame("channel_recommended"),
            ui.download_button("channel_download", "Download Campaign Plan"),
        ),
        create_footer(),
    )
