import syft as sy
import pandas as pd
from shiny import App, ui, reactive, render

login_ui = ui.page_fluid(
    ui.h1("GUEHDS Portal"),
    ui.h2("Tenant Login"),
    ui.input_text("url", "URL"),
    ui.input_text("port", "Port"),
    ui.input_text("email", "Email"),
    ui.input_password("password", "Password"),
    ui.input_action_button("login", "Login")
)

datasets_ui = ui.page_fluid(
    ui.h1("GUEHDS Portal"),
    ui.h2("Datasets"),
    ui.output_table("datasets_table")
)

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
        try:
            client = sy.login(
                url=input.url(),
                port=input.port(),
                email=input.email(),
                password=input.password()
            )
            print("Login successful!")
            login_status.set(True)
            session.client = client
        except Exception as e:
            print(f"Login failed: {e}")

    @output
    @render.table
    def datasets_table():
        if login_status():
            datasets = session.client.datasets
            data = [
                {
                    "id": dataset.id,
                    "name": dataset.name,
                    "updated_at": dataset.updated_at,
                    "created_at": dataset.created_at
                }
                for dataset in datasets
            ]
            df = pd.DataFrame(data)
            print("Datasets table rendered")
            return df

app = App(ui.output_ui("main_page"), server)
