import pandas as pd
from shiny import reactive, render, ui
from governance_ui.view import login_ui, dashboards_ui
from governance_ui.auth.login import login
from governance_ui.sections import sections
from governance_ui.federated_operations.datasets import get_datasets_table, register_dataset

def server(input, output, session):
    login_status = reactive.Value(False)
    current_section = reactive.Value("datasets")

    @output
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
        client = login(input.url(), input.port(), input.email(), input.password())
        if client:
            login_status.set(True)
            session.client = client

    @output
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

    @output
    @render.ui
    def content_ui():
        return sections[current_section()]["ui"]

    @output
    @render.ui
    def datasets_content():
        if login_status():
            datasets = session.client.datasets.get_all()
            if len(datasets) > 0:
                return ui.output_table("datasets_table")
            else:
                return ui.h4("No datasets available.", class_="text-center")

    @output
    @render.table
    def datasets_table():
        datasets = session.client.datasets
        return get_datasets_table(datasets)

    @reactive.effect
    @reactive.event(input.register_dataset)
    def handle_register_dataset():
        data_path = input.data() or input.url()
        register_dataset(
            session.client,
            input.dataset_name(),
            input.dataset_description(),
            input.asset_name(),
            input.asset_description(),
            data_path
        )
