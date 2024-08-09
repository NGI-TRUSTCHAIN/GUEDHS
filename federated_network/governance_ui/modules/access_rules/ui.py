from shiny import module, ui
from pathlib import Path


@module.ui
def access_rules_ui():
    return ui.page_fluid(
        ui.include_css(Path(__file__).parent / "../../styles.css"),
        ui.output_ui("access_rules_main"),
    )
