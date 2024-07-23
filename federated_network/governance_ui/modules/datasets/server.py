from shiny import module, render, ui, reactive
from shiny_validate import InputValidator, check
import pandas as pd
from governance_ui.federated_operations.datasets import (
    get_datasets,
    get_dataset_info,
    register_dataset,
)
from governance_ui.icons import search_icon


@module.server
def datasets_server(input, output, session, show_datasets_button):
    datasets = reactive.Value([])
    mock_data = reactive.Value(pd.DataFrame())
    current_dataset_id = reactive.Value(None)
    registered_handlers = set()

    @render.ui
    @reactive.event(show_datasets_button, ignore_none=False)
    def datasets_left():
        current_dataset_id.set(None)
        datasets.set(get_datasets(session._parent.client))
        if len(datasets()) > 0:
            return ui.output_ui("datasets_table")
        else:
            return ui.h4("No datasets available", class_="text-center")

    @render.ui
    def datasets_table():
        table_rows = []
        for dataset in datasets():
            inspect_button = ui.input_action_button(
                f"inspect_dataset_{dataset['id']}",
                ui.div(
                    ui.span(search_icon, class_="table-icon-button"),
                    ui.span("Inspect"),
                    class_="d-flex justify-content-center align-items-center",
                ),
                class_="btn btn-primary btn-sm",
            )

            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(dataset["name"]),
                    ui.tags.td(str(dataset["created_at"])),
                    ui.tags.td(str(dataset["updated_at"])),
                    ui.tags.td(inspect_button),
                )
            )
            if dataset["id"] not in registered_handlers:
                handle_inspect_dataset(dataset["id"])
                registered_handlers.add(dataset["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Name"),
                        ui.tags.th("Created At"),
                        ui.tags.th("Update At"),
                        ui.tags.th(""),
                    ),
                ),
                ui.tags.tbody(*table_rows),
                class_="smaller-table",
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )

    def handle_inspect_dataset(dataset_id):
        @reactive.effect
        @reactive.event(input[f"inspect_dataset_{dataset_id}"])
        def inspect_dataset():
            current_dataset_id.set(dataset_id)

    @render.ui
    @reactive.event(show_datasets_button, current_dataset_id, ignore_none=False)
    def dataset_info():
        if current_dataset_id() is None:
            return ui.div(
                ui.h4("Select a dataset for more details", class_="text-center"),
                style="width: 100%;\
                       height: 100%;\
                       display: flex;\
                       justify-content: center;\
                       align-items: center;",
            )

        dataset_info = get_dataset_info(session._parent.client, current_dataset_id())

        mock_data.set(dataset_info["mock_df"])

        return ui.div(
            ui.h4("Dataset Info", style="margin: 16px 0 8px;"),
            ui.div(
                ui.p("Dataset name:", class_="info-title"),
                ui.p(dataset_info["dataset_name"]),
                class_="info-container",
            ),
            ui.div(
                ui.p("Dataset description:", class_="info-title"),
                ui.p(f"{dataset_info['dataset_description'] or 'No description'}"),
                class_="info-container",
            ),
            ui.h4("Asset Info", style="margin: 20px 0 8px;"),
            ui.div(
                ui.p("Asset name:", class_="info-title"),
                ui.p(dataset_info["asset_name"]),
                class_="info-container",
            ),
            # ui.div(
            #     ui.p("Description:", class_="info-title"),
            #     ui.p(dataset_info["asset_description"]),
            #     style="font-size: 16px; display: flex; flex-wrap: wrap;"
            # ),
            ui.div(
                ui.p("Data subject:", class_="info-title"),
                ui.p(dataset_info["data_subject"]),
                class_="info-container",
            ),
            ui.div(
                ui.p("Data shape:", class_="info-title"),
                ui.p(
                    dataset_info["data_shape"][0],
                    " rows x ",
                    dataset_info["data_shape"][1],
                    " columns",
                ),
                class_="info-container",
            ),
            ui.div(
                ui.p("Mock shape:", class_="info-title"),
                ui.p(
                    dataset_info["mock_shape"][0],
                    " rows x ",
                    dataset_info["mock_shape"][1],
                    " columns",
                ),
                class_="info-container",
            ),
            ui.div(
                ui.p("Mock is real:", class_="info-title"),
                ui.p(dataset_info["mock_is_real"]),
                class_="info-container",
            ),
            ui.p("Mock preview:", style="font-weight: bold; margin-bottom: 8px;"),
            ui.output_data_frame("mock_df"),
            style="width: 100%; height: 100%; display: flex; flex-direction: column; padding: 0 16px;",
        )

    @render.data_frame
    def mock_df():
        return render.DataGrid(mock_data(), width="100%")

    @reactive.effect
    @reactive.event(input.register_dataset)
    def handle_register_dataset():
        input_validator = InputValidator()
        input_validator.enable()
        input_validator.add_rule("dataset_name", check.required())
        input_validator.add_rule("asset_name", check.required())

        def validate_data_fields(value):
            data_url = input.data_url()
            data_file = input.data_file()
            if not data_url and not data_file:
                return "Either Data URL or Data File must be provided."
            return None

        input_validator.add_rule("data_url", validate_data_fields)
        input_validator.add_rule("data_file", validate_data_fields)

        if input_validator.is_valid():
            data_path = input.data_file() or input.data_url()
            mock_path = input.mock_file() or input.mock_url() or None

            register_dataset(
                session._parent.client,
                input.dataset_name(),
                input.dataset_description(),
                input.asset_name(),
                input.asset_description(),
                data_path,
                mock_path,
                input.mock_is_real(),
            )

            ui.notification_show("Dataset registered successfully!", duration=3)
