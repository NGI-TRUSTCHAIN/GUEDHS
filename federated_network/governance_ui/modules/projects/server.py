from shiny import module, render, ui, reactive
from datetime import datetime
from governance_ui.federated_operations.projects import (
    get_projects,
    get_all_requests_by_project_id,
    get_request_by_project_id,
    execute_code,
    approve_request,
    reject_request,
)
from governance_ui.icons import arrow_left, warning_icon, search_icon, refresh_icon


@module.server
def projects_server(input, output, session, projects_button):
    projects = reactive.Value(None)
    current_project_index = reactive.Value(None)
    requests = reactive.Value([])
    current_request_index = reactive.Value(None)
    registered_handlers = set()
    request = reactive.Value({})
    global_real_result = reactive.Value(None)
    request_finished = reactive.Value(None)

    @render.ui
    @reactive.event(projects_button, current_project_index, current_request_index, ignore_none=False)
    def projects_page():
        if current_request_index() is not None:
            return ui.output_ui("request_info")
        if current_project_index() is not None:
            return ui.output_ui("project_info")
        else:
            return ui.output_ui("projects_table")

    @reactive.effect
    @reactive.event(projects_button, input.refresh_button)
    def refresh_projects():
        projects.set(get_projects(session._parent.client))

    @render.ui
    def projects_table():
        if projects() is None:
            return ui.div(
                ui.h2("Loading..."),
                ui.input_action_button("refresh_button", "", class_="disabled-button"),
                class_="d-flex w-100 h-100 justify-content-center align-items-center",
            )

        return ui.div(
            ui.h1("Projects", class_="text-center my-5"),
            ui.output_ui("projects_table_content"),
            ui.input_action_button(
                "refresh_button",
                refresh_icon,
                class_="custom-button",
                style="margin-top: 24px;",
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )

    @render.ui
    def projects_table_content():
        if projects() == []:
            return ui.h4("No projects available.", class_="text-center")

        table_rows = []
        for project in projects():
            short_description = (
                project["description"][:30] + "..." if len(project["description"]) > 30 else project["description"]
            )

            inspect_button = ui.input_action_button(
                f"inspect_project_{project['index']}",
                ui.div(
                    ui.span(search_icon, class_="table-icon-button"),
                    ui.span("Inspect"),
                    class_="d-flex justify-content-center align-items-center",
                ),
                class_="btn btn-primary btn-sm",
            )

            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(project["name"]),
                    ui.tags.td(short_description),
                    ui.tags.td(project["created_by"]),
                    ui.tags.td(project["total_requests"], style="text-align: center;"),
                    ui.tags.td(project["pending_requests"], style="text-align: center;"),
                    ui.tags.td(inspect_button),
                )
            )

            if project["id"] not in registered_handlers:
                handle_inspect_project(project["index"])
                registered_handlers.add(project["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Name"),
                        ui.tags.th("Description"),
                        ui.tags.th("Created By"),
                        ui.tags.th("Total Requests"),
                        ui.tags.th("Pending Requests"),
                        ui.tags.th(""),
                    )
                ),
                ui.tags.tbody(*table_rows),
                class_="bigger-table",
            ),
            class_="d-flex w-100 mh-75 overflow-auto justify-content-center align-items-center",
        )

    def handle_inspect_project(project_index):
        @reactive.effect
        @reactive.event(input[f"inspect_project_{project_index}"])
        def inspect_handler():
            current_project_index.set(project_index)

    @render.ui
    @reactive.event(current_project_index)
    def project_info():
        if current_project_index() is None:
            return None

        project = projects()[current_project_index()]
        requests.set(project["requests"])

        return ui.div(
            ui.input_action_button(
                "first_back_button",
                arrow_left,
                class_="custom-button position-absolute z-1 p-0",
            ),
            ui.h1(project["name"], class_="text-center my-5"),
            ui.div(
                ui.div(
                    ui.div(
                        ui.p("Description:", class_="info-title"),
                        ui.p(project["description"]),
                        class_="info-container",
                    ),
                    ui.div(
                        ui.p("Created by:", class_="info-title"),
                        ui.p(project["created_by"]),
                        class_="info-container",
                    ),
                    style="width: 80%;",
                ),
                class_="d-flex w-100 justify-content-center",
            ),
            ui.h3("Requests", class_="text-center mt-3 mb-4"),
            ui.div(
                ui.output_ui("requests_table"),
                class_="d-flex w-100 justify-content-center",
            ),
            class_="d-flex flex-column w-100 h-100",
        )

    @reactive.effect
    @reactive.event(input.refresh_requests_button)
    def refresh_requests():
        project_id = projects()[current_project_index()]["id"]
        requests.set(get_all_requests_by_project_id(session._parent.client, project_id))

    @render.ui
    def requests_table():
        if requests() is None:
            return ui.div(
                ui.h2("Loading..."),
                ui.input_action_button("refresh_requests_button", "", class_="disabled-button"),
                class_="d-flex w-100 h-100 justify-content-center align-items-center",
            )

        return ui.div(
            ui.output_ui("requests_table_content"),
            ui.input_action_button(
                "refresh_requests_button",
                refresh_icon,
                class_="custom-button",
                style="margin-top: 24px;",
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )

    @render.ui
    def requests_table_content():
        if requests() == []:
            return ui.p(
                "No requests available",
                style="font-size: 22px; margin: 18px 0; text-align: center;",
            )

        table_rows = []
        for request in requests():
            request_time = request["request_time"].utc_timestamp
            formatted_date = datetime.utcfromtimestamp(request_time).strftime("%Y-%m-%d %H:%M")

            inspect_button = ui.input_action_button(
                f"inspect_request_{request['index']}",
                ui.div(
                    ui.span(search_icon, class_="table-icon-button"),
                    ui.span("Inspect"),
                    class_="d-flex justify-content-center align-items-center",
                ),
                class_="btn btn-primary btn-sm",
            )

            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(request["description"]),
                    ui.tags.td(str(formatted_date)),
                    ui.tags.td(
                        ui.tags.div(
                            request["requesting_user_name"],
                            ui.tags.br(),
                            f"({request['requesting_user_email']})",
                        )
                    ),
                    ui.tags.td(str(request["status"])),
                    ui.tags.td(inspect_button),
                )
            )

            if request["id"] not in registered_handlers:
                handle_inspect_request(request["index"])
                registered_handlers.add(request["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Description"),
                        ui.tags.th("Request At"),
                        ui.tags.th("Requested By"),
                        ui.tags.th("Status"),
                        ui.tags.th(""),
                    ),
                ),
                ui.tags.tbody(*table_rows),
                class_="bigger-table",
            ),
            class_="d-flex w-100 mh-50 overflow-auto justify-content-center align-items-center",
        )

    @reactive.effect
    @reactive.event(input.first_back_button)
    def first_back_button_handler():
        current_project_index.set(None)
        current_request_index.set(None)

    @reactive.effect
    @reactive.event(input.second_back_button)
    def second_back_button_handler():
        current_request_index.set(None)

    def handle_inspect_request(request_index):
        @reactive.effect
        @reactive.event(input[f"inspect_request_{request_index}"])
        def inspect_request_handler():
            current_request_index.set(request_index)
            request.set(requests()[request_index])

    @reactive.effect
    @reactive.event(request_finished)
    def refresh_request():
        print("Refreshing request")
        project_id = projects()[current_project_index()]["id"]
        updated_request = get_request_by_project_id(session._parent.client, project_id, current_request_index())
        request.set(updated_request)

    @render.ui
    # @reactive.event(current_request_index, request_finished)
    def request_info():
        if current_request_index() is None:
            return None

        # request.set(requests()[current_request_index()])

        if request()["status"] == "PENDING" and request_finished() is True:
            request_finished.set(False)

        request_time = request()["request_time"].utc_timestamp
        formatted_request_date = datetime.utcfromtimestamp(request_time).strftime("%Y-%m-%d %H:%M")

        return ui.div(
            ui.input_action_button(
                "second_back_button",
                arrow_left,
                class_="custom-button position-absolute z-1 p-0",
            ),
            ui.h1(f"Request #{current_request_index() + 1}", class_="text-center mt-3 mb-5"),
            ui.div(
                ui.div(
                    ui.h4("Request Details", class_="mb-3"),
                    ui.div(
                        ui.p("Id:", class_="info-title"),
                        ui.p(request()["id"], class_="mb-0"),
                        class_="info-container",
                    ),
                    ui.div(
                        ui.p("Description:", class_="info-title"),
                        ui.p(request()["description"], class_="mb-0"),
                        class_="info-container",
                    ),
                    ui.div(
                        ui.p("Requested by:", class_="info-title"),
                        ui.p(
                            f"{request()['requesting_user_name']} ({request()['requesting_user_email']})", class_="mb-0"
                        ),
                        class_="info-container",
                    ),
                    ui.div(
                        ui.p("Requested at:", class_="info-title"),
                        ui.p(formatted_request_date, class_="mb-0"),
                        class_="info-container",
                    ),
                    ui.div(
                        ui.p("Status:", class_="info-title"),
                        ui.p(request()["status"], class_="mb-0"),
                        class_="info-container",
                    ),
                    ui.div(
                        ui.h4("Function to Analyze", class_="mb-3"),
                        ui.div(
                            ui.div(
                                ui.output_code("render_code"),
                                style="max-height: 350px; overflow: auto;",
                            ),
                            ui.output_ui("approval_section"),
                            style="width: 90%;",
                        ),
                        style="margin-top: 50px;",
                    ),
                    class_="d-flex flex-column w-50 h-100",
                ),
                ui.div(
                    ui.output_ui("dataset_info"),
                    class_="d-flex flex-column overflow-auto w-50 h-100",
                ),
                class_="d-flex flex-row h-100 overflow-auto",
            ),
            class_="d-flex flex-column w-100 h-100",
        )

    @render.ui
    def dataset_info():
        if request()["datasets"][0] == {}:
            return ui.div(
                ui.h3("No dataset required for this function."),
                class_="d-flex h-100 w-100 justify-content-center align-items-center",
                style="margin-bottom: 64px;",
            )

        dataset_time = request()["datasets"][0]["created_at"].utc_timestamp
        formatted_dataset_date = datetime.utcfromtimestamp(dataset_time).strftime("%Y-%m-%d %H:%M")

        return ui.div(
            ui.h4("Dataset Details", class_="mb-3"),
            ui.div(
                ui.p("Asset name:", class_="info-title"),
                ui.p(request()["datasets"][0]["asset_name"], class_="mb-0"),
                class_="info-container",
            ),
            ui.div(
                ui.p("Dataset uploaded by:", class_="info-title"),
                ui.p(
                    f"{request()['datasets'][0]['uploader_name']} ({request()['datasets'][0]['uploader_email']})",
                    class_="mb-0",
                ),
                class_="info-container",
            ),
            ui.div(
                ui.p("Created at:", class_="info-title"),
                ui.p(formatted_dataset_date, class_="mb-0"),
                class_="info-container",
            ),
            ui.div(
                ui.p("Private Data Preview:", class_="info-title mb-1"),
                ui.output_data_frame("pvt_data_df"),
                class_="w-100",
            ),
            ui.div(
                ui.p("Mock Data Preview:", class_="info-title mt-3 mb-1"),
                ui.output_data_frame("mock_df"),
                class_="w-100",
            ),
        )

    @render.data_frame
    def pvt_data_df():
        pvt_data_df = request()["datasets"][0]["private_data"]
        return render.DataGrid(pvt_data_df, width="100%")

    @render.data_frame
    def mock_df():
        mock_df = request()["datasets"][0]["mock_data"]
        return render.DataGrid(mock_df, width="100%")

    @render.code
    def render_code():
        return request()["function_code"]

    @render.ui
    def approval_section():
        if request()["status"] == "PENDING":
            return ui.div(
                ui.div(
                    ui.span(warning_icon),
                    ui.p(
                        "It is the Data Owner's responsibility to review the code and\
                         verify if it's safe to execute it and approve the request!",
                        style="font-weight: bold; margin-bottom: 0px;",
                    ),
                    class_="d-flex flex-row gap-3 justify-content-center align-items-center",
                    style="width: 80%; margin-bottom: 16px;",
                ),
                ui.div(
                    ui.input_action_button(
                        "execute_button",
                        "Execute",
                        class_="btn btn-secondary",
                    ),
                    ui.input_action_button(
                        "reject_button",
                        "Reject",
                        class_="btn btn-danger",
                    ),
                    class_="d-flex flex-row gap-5",
                ),
                class_="d-flex flex-column justify-content-center align-items-center",
                style="margin-top: 32px;",
            )

    @reactive.effect
    @reactive.event(input.execute_button)
    def execute_button_handler():
        project_id = projects()[current_project_index()]["id"]
        mock_result, real_result = execute_code(session._parent.client, project_id, current_request_index())
        global_real_result.set(real_result)

        modal = ui.modal(
            ui.div(
                ui.div(
                    ui.output_code("render_code"),
                    style="max-height: 350px; overflow: auto;",
                ),
                ui.div(
                    ui.p("Mock result:", class_="info-title"),
                    ui.p(mock_result, class_="mb-0"),
                    class_="info-container pt-3",
                ),
                ui.div(
                    ui.p("Real result:", class_="info-title"),
                    ui.p(real_result, class_="mb-0"),
                    class_="info-container pb-3",
                ),
                ui.div(
                    ui.input_action_button(
                        "approve_button",
                        "Approve",
                        class_="btn btn-success",
                    ),
                    ui.input_action_button(
                        "reject_button",
                        "Reject",
                        class_="btn btn-danger",
                    ),
                    class_="d-flex flex-row gap-5 justify-content-center align-items-center",
                ),
                class_="d-flex flex-column",
            ),
            title="Function executed successfully! Review the results and approve or reject the request.",
            footer=None,
            size="l",
            easy_close=True,
        )
        ui.modal_show(modal)

    @reactive.effect
    @reactive.event(input.approve_button)
    def approve_button_handler():
        project_id = projects()[current_project_index()]["id"]
        approve_request(session._parent.client, project_id, current_request_index(), global_real_result())
        ui.modal_remove()
        request_finished.set(True)

    @reactive.effect
    @reactive.event(input.reject_button)
    def reject_button_handler():
        project_id = projects()[current_project_index()]["id"]
        reject_request(session._parent.client, project_id, current_request_index(), "")
        ui.modal_remove()
        request_finished.set(True)
