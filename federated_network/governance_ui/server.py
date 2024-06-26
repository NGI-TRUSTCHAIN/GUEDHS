import pandas as pd
from shiny import reactive, render, ui
from governance_ui.view import login_ui, dashboards_ui, datasets_ui, create_dataset_ui
from governance_ui.auth.login import login

def server(input, output, session):
    login_status = reactive.Value(False)
    show_datasets = reactive.Value(True)
    show_create_dataset = reactive.Value(False)

    @output
    @render.ui
    def main_page():
        client = login("localhost", "8081", "info@openmined.org", "changethis")
        login_status.set(True)
        session.client = client
        return dashboards_ui
        # if not login_status():
        #     print("Rendering login UI")
        #     return login_ui
        # else:
        #     print("Rendering datasets UI")
        #     return dashboards_ui

    @reactive.effect
    @reactive.event(input.login)
    def handle_login():
        client = login(input.url(), input.port(), input.email(), input.password())
        if client:
            login_status.set(True)
            session.client = client

    @reactive.effect
    @reactive.event(input.show_datasets_button)
    def handle_show_datasets():
        show_datasets.set(True)
        show_create_dataset.set(False)

    @reactive.effect
    @reactive.event(input.create_dataset_button)
    def handle_create_datasets():
        show_datasets.set(False)
        show_create_dataset.set(True)

    # def handle_section(section):
    #     @reactive.effect
    #     @reactive.event(input[section])
    #     # def section_handler():

    #     return section_handler

    @output
    @render.ui
    def content_ui():
        if show_datasets():
            return datasets_ui
        elif show_create_dataset():
            return create_dataset_ui

    @output
    @render.ui
    def datasets_content():
        if login_status():
            datasets = session.client.datasets
            if not datasets:
                return ui.h4("No datasets available.", class_="text-center")
            else:
                return ui.output_table("datasets_table")

    @output
    @render.table
    def datasets_table():
        datasets = session.client.datasets
        data = [
            {
                "id": dataset.id,
                "name": dataset.name,
                "updated at": dataset.updated_at,
                "created at": dataset.created_at
            }
            for dataset in datasets
        ]
        return pd.DataFrame(data)

