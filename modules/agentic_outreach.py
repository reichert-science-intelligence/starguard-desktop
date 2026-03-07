"""
AI-Generated Member Outreach
Phase 1 Week 2: Agentic message generation with Anthropic Claude.
"""

from shiny import ui

from modules.shared_ui import create_footer, create_header

TONE_CHOICES = {
    "Empathetic": "Empathetic",
    "Urgent": "Urgent",
    "Educational": "Educational",
    "Incentive-Focused": "Incentive-Focused",
}


def agentic_outreach_content():
    """UI for AI-Generated Member Outreach."""
    return ui.TagList(
        create_header(),
        ui.card(
            ui.card_header("AI-Generated Member Outreach"),
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select(
                        "outreach_sample_member",
                        "Select Member",
                        choices={"": "Loading..."},
                    ),
                    ui.input_select(
                        "outreach_message_tone",
                        "Message Tone",
                        choices=TONE_CHOICES,
                    ),
                    ui.input_action_button(
                        "outreach_generate",
                        "Generate Message",
                        class_="btn-success",
                    ),
                    width=250,
                ),
                ui.div(
                    ui.output_ui("outreach_member_context"),
                    ui.output_text_verbatim("outreach_generated_message"),
                    ui.output_ui("outreach_message_analysis"),
                ),
            ),
        ),
        create_footer(),
    )
