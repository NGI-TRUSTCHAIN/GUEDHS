from shiny import reactive, render, ui
from pathlib import Path
from governance_ui.sections import sections
from governance_ui.modules.auth import auth_ui, auth_server
from governance_ui.modules.datasets import datasets_server
from governance_ui.modules.projects import projects_server
from governance_ui.modules.users import users_server
from governance_ui.modules.audit_logs import audit_logs_server
from governance_ui.modules.access_rules import access_rules_server
from governance_ui.icons import logout_icon

dashboards_ui = ui.page_sidebar(
    ui.sidebar(
        ui.include_css(Path(__file__).parent / "styles.css"),
        ui.h4("GUEHDS Portal", class_="text-center my-4"),
        ui.output_ui("sidebar_buttons"),
        style="background-color: #e5e7eb; height: 100vh; box-shadow: 0 4px 8px rgba(0,0,0,0.1);",
    ),
    ui.output_ui("content_ui"),
    style="background-color: #f3f4f6 !important; height: 100vh;",
)


def server(input, output, session):
    current_section = reactive.Value("datasets")
    client = reactive.Value(None)

    @render.ui
    @reactive.event(client, ignore_none=False)
    def main_page():
        if client():
            session.client = client()
            return dashboards_ui
        else:
            return auth_ui("login")

    auth_server("login", client=client)

    @render.ui
    def sidebar_buttons():
        return ui.div(
            ui.div(
                [
                    ui.input_action_button(
                        section["button_id"],
                        ui.div(
                            ui.span(section["icon"], class_="table-icon-button"),
                            ui.span(section["button_text"]),
                            class_="d-flex justify-content-start align-items-center",
                        ),
                        class_="btn btn-primary mb-3",
                        style="width: 220px;",
                    )
                    for section in sections.values()
                ]
            ),
            ui.div(
                ui.input_action_button(
                    "logout_button",
                    ui.div(
                        ui.span(logout_icon, style="margin-right: 12px;"),
                        ui.span("Logout"),
                        class_="d-flex justify-content-start align-items-center",
                    ),
                    class_="btn btn-secondary",
                    style="width: 200px;",
                ),
                style="margin-bottom: 8px;",
            ),
            style="display: flex;\
                   flex-direction: column;\
                   height: 100%;\
                   align-items: center;\
                   justify-content: space-between;",
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

    @reactive.effect
    @reactive.event(input.logout_button)
    async def logout_button_handler():
        print("Logging out")
        await session.send_custom_message("logout", None)

    datasets_server("datasets", show_datasets_button=input.list_datasets_button)

    projects_server("projects", projects_button=input.projects_button)

    access_rules_server("access_rules")

    users_server("users", users_button=input.list_users_button)

    audit_logs_server("audit_logs", audit_button=input.audit_logs_button)
