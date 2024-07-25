from shiny import module, render, ui, reactive
from governance_ui.federated_operations.audit_logs import get_audit_logs
from governance_ui.icons import search_icon
import json


@module.server
def audit_logs_server(input, output, session, audit_button):
    audit_logs = reactive.Value(None)
    current_log_index = reactive.Value(None)
    registered_handlers = set()

    @reactive.effect
    @reactive.event(audit_button, input.apply_filters_button)
    def audit_logs_filtered_table():
        filters = []
        if input.filter_list():
            filters.append("listActions")
        if input.filter_inspect():
            filters.append("inspectActions")
        if input.filter_create():
            filters.append("createActions")
        if input.filter_update():
            filters.append("updateActions")
        if input.filter_delete():
            filters.append("deleteActions")

        audit_logs.set(get_audit_logs(filters))

    @render.ui
    def audit_logs_table():
        if audit_logs() == []:
            return ui.div(
                ui.h1("Audit Logs", class_="text-center my-5"),
                ui.h4("No logs available.", class_="text-center"),
                class_="d-flex flex-column w-100 h-100 align-items-center",
            )

        table_row = []
        for log in audit_logs():
            inspect_button = ui.input_action_button(
                f"inspect_log_{log['index']}",
                ui.div(
                    ui.span(search_icon, class_="table-icon-button"),
                    ui.span("Inspect"),
                    class_="d-flex justify-content-center align-items-center",
                ),
                class_="btn btn-primary btn-sm",
            )

            table_row.append(
                ui.tags.tr(
                    ui.tags.td(log["timestamp"]),
                    ui.tags.td(log["action_type"]),
                    ui.tags.td(log["action"]),
                    ui.tags.td(log["dataCustodianUUID"]),
                    ui.tags.td(inspect_button),
                )
            )

            if log["index"] not in registered_handlers:
                handle_inspect_log(log["index"])
                registered_handlers.add(log["index"])

        return ui.div(
            ui.h1("Audit Logs", class_="text-center my-5"),
            ui.div(
                ui.tags.table(
                    ui.tags.thead(
                        ui.tags.tr(
                            ui.tags.th("Timestamp"),
                            ui.tags.th("Action Type"),
                            ui.tags.th("Action"),
                            ui.tags.th("Data Custodian"),
                            ui.tags.th(""),
                        )
                    ),
                    ui.tags.tbody(*table_row),
                    style="width: 100%; !important;",
                    class_="bigger-table",
                ),
                class_="h-75 overflow-auto",
                style="width: 90%;",
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )

    def handle_inspect_log(index):
        @reactive.effect
        @reactive.event(input[f"inspect_log_{index}"], ignore_init=True)
        def inspect_log_handler():
            print("Inspecting log", index)
            current_log_index.set(index)

    @reactive.effect
    @reactive.event(current_log_index)
    def show_modal():
        print("Current log index", current_log_index())
        modal = ui.modal(
            ui.div(
                ui.output_code("render_json"),
            ),
            title="Inspect Log",
            footer=None,
            size="l",
            easy_close=True,
        )
        ui.modal_show(modal)

    @render.code
    def render_json():
        log_json = audit_logs()[current_log_index()]["json"]
        return json.dumps(log_json, indent=4)
