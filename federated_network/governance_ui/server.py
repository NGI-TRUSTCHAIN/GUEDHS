import pandas as pd
from shiny import reactive, render, ui
from governance_ui.view import login_ui, dashboards_ui
from governance_ui.auth.login import login
from governance_ui.sections import sections

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
                "id": f"{str(dataset.id)[:8]}...",
                "name": dataset.name,
                "updated at": dataset.updated_at,
                "created at": dataset.created_at
            }
            for dataset in datasets
        ]

        df = pd.DataFrame(data)
        styled_df = df.style.hide(axis="index").set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#e5e7eb"),
                        ("padding", "10px 15px"),
                    ]
                },
                {
                    "selector": "td",
                    "props": [
                        ("background-color", "#f3f4f6"),
                        ("padding", "10px 15px")
                    ]
                }
            ]
        ).set_table_attributes(
            'style="border-radius: 10px; overflow: hidden;"'
        )

        return styled_df
