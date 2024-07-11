from shiny import module, render, ui, reactive
from shiny.types import ImgData
from datetime import datetime
from pathlib import Path
from governance_ui.federated_operations.projects import get_projects, get_project_info


@module.server
def projects_server(input, output, session, projects_button):
    projects = reactive.Value([])
    current_project_id = reactive.Value(None)
    current_request_id = reactive.Value(None)
    registered_handlers = set()
    table_rows = reactive.Value([])

    @render.ui
    @reactive.event(projects_button, current_project_id, ignore_none=False)
    def projects_page():
        projects.set(get_projects(session._parent.client))
        if current_project_id() is not None:
            return ui.output_ui("project_info")
        elif len(projects()) > 0:
            return ui.output_ui("projects_table")
        else:
            return ui.h4("No projects available.", class_="text-center")

    @render.ui
    def projects_table():
        table_rows = []
        for project in projects():
            inspect_button = ui.input_action_button(f"inspect_project_{project['id']}", "Inspect", class_="btn btn-primary btn-sm")
            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(project["name"]),
                    ui.tags.td(project["description"]),
                    ui.tags.td(project["created_by"]),
                    ui.tags.td(project["pending_requests"], style="text-align: center;"),
                    ui.tags.td(inspect_button),
                )
            )
            if project["id"] not in registered_handlers:
                handle_inspect_project(project["id"])
                registered_handlers.add(project["id"])

        return ui.div(
            ui.h1("Projects", class_="text-center my-5"),
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Name"),
                        ui.tags.th("Description"),
                        ui.tags.th("Created By"),
                        ui.tags.th("Pending Requests"),
                        ui.tags.th(""),
                    )
                ),
                ui.tags.tbody(*table_rows),
                class_="bigger-table",
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )

    def handle_inspect_project(project_id):
        @reactive.effect
        @reactive.event(input[f"inspect_project_{project_id}"])
        def inspect_handler():
            current_project_id.set(project_id)

    @render.ui
    @reactive.event(current_request_id, current_project_id)
    def project_info():
        project = get_project_info(session._parent.client, current_project_id())

        requests = project["requests"]
        rows = []
        for request in requests:
            request_time = request["request_time"].utc_timestamp
            formatted_date = datetime.utcfromtimestamp(request_time).strftime("%Y-%m-%d %H:%M")
            inspect_button = ui.input_action_button(f"inspect_request_{request['id']}", "Inspect", class_="btn btn-primary btn-sm")
            rows.append(
                ui.tags.tr(
                    ui.tags.td(request["description"]),
                    ui.tags.td(str(formatted_date)),
                    ui.tags.td(ui.tags.div(request["requesting_user_name"], ui.tags.br(), request["requesting_user_email"])),
                    ui.tags.td(str(request["status"])),
                    ui.tags.td(inspect_button),
                )
            )
            if request["id"] not in registered_handlers:
                handle_inspect_request(request["id"])
                registered_handlers.add(request["id"])

        table_rows.set(rows)

        return ui.page_fluid(
            ui.div(
                ui.card(
                    ui.input_action_button(
                        "back_button",
                        ui.output_image("back_button_image"),
                        style="position: absolute; z-index: 1; width: 40px; height: 40px; background: none; border: none; padding: 0;",
                    ),
                    ui.h3(project["project_name"], class_="text-center mt-5 mb-3"),
                    ui.div(
                        ui.div(
                            ui.div(
                                ui.p("Description:", style="font-weight: bold; margin: 0 8px 0 0;"),
                                ui.p(project["project_description"]),
                                style="font-size: 16px; display: flex; flex-wrap: wrap; margin-bottom: 8px;",
                            ),
                            ui.div(
                                ui.p("Created by:", style="font-weight: bold; margin: 0 8px 0 0;"),
                                ui.p(project["created_by"]),
                                style="font-size: 16px; display: flex; flex-direction: row; flex-wrap: wrap; margin-bottom: 8px;",
                            ),
                        ),
                        ui.p("Requests:", style="font-weight: bold; font-size: 18px; margin: 32px 0 12px 0;"),
                        ui.output_ui("requests_table"),
                        class_="w-100",
                    ),
                    height="90%",
                ),
                class_="d-flex flex-column w-50 h-100 px-3 justify-content-center",
            ),
            ui.div(
                ui.card(
                    ui.output_ui("request_info"),
                    height="90%",
                ),
                class_="w-50 h-100 d-flex flex-column justify-content-center",
            ),
            class_="d-flex flex-row h-100 gap-5 px-3",
        )

    @render.ui
    def requests_table():
        if table_rows() == []:
            return ui.p("No requests available", style="font-size: 22px; margin: 18px 0; text-align: center;")

        return (
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Description"),
                        ui.tags.th("Request Time"),
                        ui.tags.th("Requested By"),
                        ui.tags.th("Status"),
                        ui.tags.th(""),
                    ),
                ),
                ui.tags.tbody(*table_rows()),
                class_="smaller-table",
            ),
        )

    @reactive.effect
    @reactive.event(input.back_button)
    def back_button_handler():
        current_project_id.set(None)
        current_request_id.set(None)

    @render.image
    def back_button_image():
        dir = Path(__file__).parent
        img: ImgData = {"src": str(dir / "back-arrow.svg"), "width": "40px"}
        return img

    def handle_inspect_request(request_id):
        @reactive.effect
        @reactive.event(input[f"inspect_request_{request_id}"])
        def inspect_request_handler():
            current_request_id.set(request_id)
            print(f"Inspecting request {request_id}")

    @render.ui
    def request_info():
        return ui.h1(str(current_request_id()), class_="text-center my-5")
