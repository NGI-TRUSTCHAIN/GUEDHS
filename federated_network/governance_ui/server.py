from shiny import reactive, render, ui
from shiny_validate import InputValidator, check
import pandas as pd
from prisma import Prisma
from governance_ui.view import login_ui, dashboards_ui
from governance_ui.auth.login import login
from governance_ui.sections import sections
from governance_ui.federated_operations.datasets import get_datasets_table, register_dataset, get_dataset_info

db = Prisma()
db.connect()


def server(input, output, session):
    login_status = reactive.Value(False)
    current_section = reactive.Value("datasets")
    datasets_data = reactive.Value(pd.DataFrame())
    mock_data = reactive.Value(pd.DataFrame())

    @render.ui
    def main_page():
        if not login_status():
            print("Rendering login UI")
            return login_ui
        else:
            print("Rendering dashboard UI")
            return dashboards_ui

    @reactive.effect
    @reactive.event(input.login)
    def handle_login():
        login_validator = InputValidator()
        login_validator.enable()
        login_validator.add_rule("url", check.required())
        login_validator.add_rule("port", check.required())
        login_validator.add_rule("email", check.required())
        login_validator.add_rule("email", check.email())
        login_validator.add_rule("password", check.required())

        if login_validator.is_valid():
            client = login(input.url(), input.port(), input.email(), input.password())
            if client:
                login_status.set(True)
                session.client = client

    @render.ui
    def sidebar_buttons():
        return ui.div(
            [
                ui.input_action_button(
                    section["button_id"],
                    section["button_text"],
                    class_="btn btn-primary mb-3",
                    style="width: 200px;",
                )
                for section in sections.values()
            ]
        )

    def handle_section(section):
        @reactive.effect
        @reactive.event(input[sections[section]["button_id"]])
        def section_handler():
            current_section.set(section)

        return section_handler

    for section in sections:
        handle_section(section)

    @render.ui
    def content_ui():
        return sections[current_section()]["ui"]

    @render.ui
    @reactive.event(input.show_datasets_button, ignore_none=False)
    def datasets_left():
        datasets_data.set(get_datasets_table(session.client))
        if len(datasets_data()) > 0:
            return ui.output_data_frame("datasets_df")
        else:
            return ui.h4("No datasets available.", class_="text-center")

    @render.data_frame
    def datasets_df():
        return render.DataGrid(datasets_data().drop("id", axis=1), width="100%", selection_mode="row")

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

        dataset_id = datasets_data().loc[selected_dataset.index[0]].id
        dataset_info = get_dataset_info(session.client, dataset_id)

        mock_data.set(dataset_info["mock_df"])

        return ui.div(
            ui.p("Dataset info:", style="font-weight: bold; font-size: 22px; margin: 16px 0 8px;"),
            ui.div(
                ui.p("Dataset name:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["dataset_name"], style="font-size: 18px;"),
                style="font-size: 18px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Dataset description:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["dataset_description"]),
                style="font-size: 18px; display: flex; flex-wrap: wrap;",
            ),
            ui.p("Asset info:", style="font-weight: bold; font-size: 22px; margin: 20px 0 8px;"),
            ui.div(
                ui.p("Asset name:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["asset_name"], style="font-size: 18px;"),
                style="font-size: 18px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            # ui.div(
            #     ui.p("Description:", style="font-weight: bold; margin: 0 8px 0 0;"),
            #     ui.p(dataset_info["asset_description"]),
            #     style="font-size: 18px; display: flex; flex-wrap: wrap; margin-bottom: 8px"
            # ),
            ui.div(
                ui.p("Data subject:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["data_subject"]),
                style="font-size: 18px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Data shape:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["data_shape"][0], " rows x ", dataset_info["data_shape"][1], " columns"),
                style="font-size: 18px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Mock shape:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["mock_shape"][0], " rows x ", dataset_info["mock_shape"][1], " columns"),
                style="font-size: 18px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.div(
                ui.p("Mock is real:", style="font-weight: bold; margin: 0 8px 0 0;"),
                ui.p(dataset_info["mock_is_real"]),
                style="font-size: 18px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
            ),
            ui.p("Mock preview:", style="font-weight: bold; font-size: 18px; margin-bottom: 8px;"),
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
                session.client,
                input.dataset_name(),
                input.dataset_description(),
                input.asset_name(),
                input.asset_description(),
                data_path,
                mock_path,
            )

            ui.notification_show("Dataset registered successfully!", duration=3)
