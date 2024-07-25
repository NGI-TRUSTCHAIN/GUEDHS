from shiny import module, ui
from pathlib import Path


@module.ui
def audit_logs_ui():
    return ui.page_fluid(
        ui.include_css(Path(__file__).parent / "../../styles.css"),
        ui.div(
            ui.card(
                ui.h4("Filters", class_="py-2 text-center"),
                ui.input_checkbox("filter_list", "List Actions", value=True),
                ui.input_checkbox("filter_inspect", "Inspect Actions", value=True),
                ui.input_checkbox("filter_create", "Create Actions", value=True),
                ui.input_checkbox("filter_update", "Update Actions", value=True),
                ui.input_checkbox("filter_delete", "Delete Actions", value=True),
                ui.div(
                    ui.input_action_button(
                        "apply_filters_button",
                        "Filter",
                        class_="btn btn-primary",
                        style="width: 150px;",
                    ),
                    class_="d-flex pt-3 pb-2 justify-content-center",
                ),
                height="50%",
                class_="d-flex flex-column",
            ),
            class_="d-flex h-100 align-items-center justify-content-center",
            style="width: 20%;",
        ),
        ui.div(
            ui.output_ui("audit_logs_table"),
            class_="d-flex flex-column h-100 align-items-center justify-content-center",
            style="width: 80%;",
        ),
        class_="d-flex flex-row h-100 w-100 gap-3 align-items-center justify-content-center",
    )
