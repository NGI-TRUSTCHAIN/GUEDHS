from shiny import reactive, render, ui
from shiny_validate import InputValidator, check
from governance_ui.view import login_ui, dashboards_ui
from governance_ui.auth.login import login
from governance_ui.sections import sections
from governance_ui.federated_operations.datasets import get_datasets_table, register_dataset

def server(input, output, session):
    login_status = reactive.Value(False)
    current_section = reactive.Value("datasets")

    @render.ui
    def main_page():
        # client = login("localhost", "8082", "info@openmined.org", "changethis")
        # login_status.set(True)
        # session.client = client
        # return dashboards_ui
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
                    style="width: 200px;"
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
    def datasets_content():
        datasets = session.client.datasets.get_all()
        if len(datasets) > 0:
            return ui.output_table("datasets_table")
        else:
            return ui.h4("No datasets available.", class_="text-center")

    @render.table
    @reactive.event(input.show_datasets_button, ignore_none=False)
    def datasets_table():
        return get_datasets_table(session.client)

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
                mock_path
            )

            ui.notification_show("Dataset registered successfully!", duration=3)
