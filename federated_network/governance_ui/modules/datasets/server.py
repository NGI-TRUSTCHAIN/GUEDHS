from shiny import module, render, ui, reactive
from shiny_validate import InputValidator, check
import pandas as pd
from governance_ui.federated_operations.datasets import get_datasets, get_dataset_info, register_dataset


@module.server
def datasets_server(input, output, session, show_datasets_button):
    datasets = reactive.Value(pd.DataFrame())
    mock_data = reactive.Value(pd.DataFrame())

    @render.ui
    @reactive.event(show_datasets_button, ignore_none=False)
    def datasets_left():
        datasets.set(get_datasets(session._parent.client))
        if len(datasets()) > 0:
            return ui.output_data_frame("datasets_df")
        else:
            return ui.h4("No datasets available.", class_="text-center")

    @render.data_frame
    def datasets_df():
        return render.DataGrid(datasets().drop("id", axis=1), width="100%", selection_mode="row")

    @reactive.calc
    def filtered_df():
        data_selected = datasets_df.data_view(selected=True)
        return data_selected

    @render.ui
    def dataset_content():
        selected_dataset = filtered_df()

        if selected_dataset.empty:
            return ui.div(
                ui.h4("Select a dataset for more details", class_="text-center"),
                style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;",
            )

        dataset_id = datasets().loc[selected_dataset.index[0]].id
        dataset_info = get_dataset_info(session._parent.client, dataset_id)

        mock_data.set(dataset_info["mock_df"])

        return ui.div(
            ui.p("Dataset info:", style="font-weight: bold; font-size: 20px; margin: 16px 0 8px;"),
            ui.div(
                ui.p("Dataset name:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["dataset_name"]),
                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Dataset description:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["dataset_description"]),
                style="font-size: 16px; display: flex; flex-wrap: wrap;",
            ),
            ui.p("Asset info:", style="font-weight: bold; font-size: 20px; margin: 24px 0 8px;"),
            ui.div(
                ui.p("Asset name:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["asset_name"]),
                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            # ui.div(
            #     ui.p("Description:", style="font-weight: bold; margin: 0 8px 0 0;"),
            #     ui.p(dataset_info["asset_description"]),
            #     style="font-size: 16px; display: flex; flex-wrap: wrap; margin-bottom: 8px"
            # ),
            ui.div(
                ui.p("Data subject:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["data_subject"]),
                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Data shape:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["data_shape"][0], " rows x ", dataset_info["data_shape"][1], " columns"),
                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Mock shape:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["mock_shape"][0], " rows x ", dataset_info["mock_shape"][1], " columns"),
                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Mock is real:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["mock_is_real"]),
                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.p("Mock preview:", style="font-weight: bold; font-size: 16px; margin-bottom: 8px;"),
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
            )

            ui.notification_show("Dataset registered successfully!", duration=3)
