from shiny import reactive, render, ui
from prisma import Prisma
from governance_ui.sections import sections
from governance_ui.modules.auth import login_ui, login_server
from governance_ui.modules.datasets import datasets_server
from governance_ui.modules.projects import projects_server
# from governance_ui.auth.login import login

db = Prisma()
db.connect()

dashboards_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("GUEHDS Portal", class_="text-center my-4"),
        ui.output_ui("sidebar_buttons"),
        style="background-color: #e5e7eb; height: 100vh; box-shadow: 0 4px 8px rgba(0,0,0,0.1);",
    ),
    ui.output_ui("content_ui"),
    style="background-color: #f3f4f6 !important; height: 100vh;",
)


def server(input, output, session):
    login_status = reactive.Value(False)
    current_section = reactive.Value("datasets")

    @render.ui
    def main_page():
        # client = login("localhost", "8081", "info@openmined.org", "changethis")
        # login_status.set(True)
        # session.client = client
        # return dashboards_ui
        if not login_status():
            print("Rendering login UI")
            return login_ui("login")
        else:
            print("Rendering dashboard UI")
            return dashboards_ui

    login_server("login", login_status=login_status)

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

    datasets_server("datasets", show_datasets_button=input.show_datasets_button)

    projects_server("projects", projects_button=input.projects_button)
