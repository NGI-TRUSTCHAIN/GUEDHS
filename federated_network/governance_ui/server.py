import pandas as pd
from shiny import reactive, render
from view import login_ui, datasets_ui
from governance_ui.auth.login import login

def server(input, output, session):
    login_status = reactive.Value(False)

    @output
    @render.ui
    def main_page():
        if not login_status():
            print("Rendering login UI")
            return login_ui
        else:
            print("Rendering datasets UI")
            return datasets_ui

    @reactive.effect
    @reactive.event(input.login)
    def _():
        client = login(input.url(), input.port(), input.email(), input.password())
        if client:
            login_status.set(True)
            session.client = client

    @output
    @render.table
    def datasets_table():
        if login_status():
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

    @output
    @render.text
    def no_datasets_message():
        if login_status():
            datasets = session.client.datasets
            if not datasets:
                return "No datasets available."
