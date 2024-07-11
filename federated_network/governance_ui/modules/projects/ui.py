from shiny import module, ui
from pathlib import Path


@module.ui
def projects_ui():
    return ui.page_fluid(
        ui.include_css(Path(__file__).parent / "../../styles.css"),
        ui.output_table("projects_page"),
        class_="d-flex flex-row h-100 gap-5 px-3 align-items-center justify-content-center",
    )
