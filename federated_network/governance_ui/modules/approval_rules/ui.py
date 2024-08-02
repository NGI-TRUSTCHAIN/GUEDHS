from shiny import module, ui
from pathlib import Path
from governance_ui.icons import add_icon, play_icon


@module.ui
def approval_rules_ui():
    return ui.page_fluid(
        ui.include_css(Path(__file__).parent / "../../styles.css"),
        ui.div(
            ui.h1("Approval Rules", class_="my-5"),
            ui.div(
                ui.tooltip(
                    ui.input_action_button("apply_rules_button", play_icon, class_="custom-button p-3"),
                    "Apply the rules",
                ),
                ui.tooltip(
                    ui.input_action_button("add_rule_button", add_icon, class_="custom-button p-3"),
                    "Add a new rule",
                ),
                class_="d-flex flex-column gap-2 position-absolute top-0 end-0 z-1",
                style="margin: 48px 48px 0 0;",
            ),
            ui.accordion(
                ui.accordion_panel("User Rules", ui.output_ui("user_rules_section"), value="user_rules"),
                ui.accordion_panel("Dataset Rules", ui.output_ui("dataset_rules_section"), value="dataset_rules"),
                ui.accordion_panel("Pair Rules", ui.output_ui("pair_rules_section"), value="pair_rules"),
                open=False,
                class_="d-flex flex-column w-75 h-75 justify-content-center",
            ),
            class_="d-flex flex-column h-100 w-100 align-items-center justify-content-center",
        ),
    )
