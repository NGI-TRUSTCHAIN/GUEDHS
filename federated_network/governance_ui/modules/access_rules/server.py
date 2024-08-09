from shiny import module, render, ui, reactive
from governance_ui.federated_operations.access_rules import (
    get_user_rules,
    get_dataset_rules,
    get_pair_rules,
    delete_rule,
    apply_rules_on_requests,
    add_rule,
)
from governance_ui.federated_operations.datasets import get_datasets_names
from governance_ui.federated_operations.projects import approve_multiple_requests, reject_multiple_requests
from governance_ui.icons import (
    add_icon,
    play_icon,
    trash_icon,
    search_icon,
    arrow_left,
    check_icon,
    check_icon_green,
    x_icon,
    x_icon_red,
)
from datetime import datetime


@module.server
def access_rules_server(input, output, session):
    show_apply_decisions_page = reactive.Value(False)
    open_accordions = reactive.Value([])
    trigger_update_rules = reactive.Value(True)
    registered_handlers = set()
    request_decisions = reactive.Value(None)
    final_decisions = reactive.Value({})
    trigger_change_decisions = reactive.Value(False)
    current_request_id = reactive.Value(None)
    final_approve_requests = reactive.Value({})
    final_reject_requests = reactive.Value({})
    toggle_inspect_modal = reactive.Value(False)

    sections = {
        "user_rules": {
            "target": "user",
            "fields": ["type", "user_id", "expires_at"],
            "columns": ["Type", "User", "Expires At"],
            "get_rules_func": get_user_rules,
        },
        "dataset_rules": {
            "target": "dataset",
            "fields": ["type", "dataset_name", "expires_at"],
            "columns": ["Type", "Dataset", "Expires At"],
            "get_rules_func": get_dataset_rules,
        },
        "pair_rules": {
            "target": "pair",
            "fields": ["type", "user_id", "dataset_name", "expires_at"],
            "columns": ["Type", "User", "Dataset", "Expires At"],
            "get_rules_func": get_pair_rules,
        },
    }

    @render.ui
    @reactive.event(show_apply_decisions_page)
    def access_rules_main():
        if show_apply_decisions_page():
            return ui.output_ui("apply_decisions_output")
        else:
            return ui.output_ui("access_rules_page")

    @render.ui
    @reactive.event(trigger_update_rules)
    def access_rules_page():
        items = [make_rules_accordion_panel(section) for section in sections]

        return (
            ui.div(
                ui.h1("Decision Rules", class_="my-5"),
                ui.div(
                    ui.tooltip(
                        ui.input_action_button("apply_rules_button", play_icon, class_="custom-button p-3"),
                        "Apply rules",
                    ),
                    ui.tooltip(
                        ui.input_action_button("add_rule_button", add_icon, class_="custom-button p-3"),
                        "Add a new rule",
                    ),
                    class_="d-flex flex-column gap-2 position-absolute top-0 end-0 z-1",
                    style="margin: 48px 48px 0 0;",
                ),
                ui.div(
                    ui.accordion(
                        *items,
                        id="rules_acc",
                        open=open_accordions() if open_accordions() else False,
                        class_="approval-accordion d-flex flex-column w-100 h-100",
                    ),
                    style="width: 75%; max-height: 75vh; overflow-y: auto;",
                ),
                class_="d-flex flex-column w-100 h-100 align-items-center",
            ),
        )

    @reactive.effect
    @reactive.event(input.rules_acc)
    def open_accordion_panels():
        open_accordions.set([panel for panel in input.rules_acc()])

    def make_rules_accordion_panel(section):
        target = sections[section]["target"]
        fields = sections[section]["fields"]
        columns = sections[section]["columns"]
        get_rules_func = sections[section]["get_rules_func"]

        return ui.accordion_panel(
            f"{target.capitalize()} Rules", handle_rule_section(target, fields, columns, get_rules_func)
        )

    def handle_rule_section(target, fields, columns, get_rules_func):
        rules = get_rules_func(session._parent.client)

        if rules == []:
            return ui.div(
                ui.h5(f"No {target} rules available.", class_="text-center my-4"),
                class_="d-flex flex-column w-100 h-100 align-items-center",
                style="background-color: #f3f4f6;",
            )

        sorted_rules = sorted(rules, key=lambda x: x["expires_at"])

        table_row = []
        for rule in sorted_rules:
            delete_rule_button = ui.input_action_button(
                f"delete_{target}_rule_{rule['index']}",
                trash_icon,
                class_="custom-button",
            )

            table_row.append(
                ui.tags.tr(
                    *[ui.tags.td(rule[field]) for field in fields],
                    ui.tags.td(delete_rule_button, style="text-align: right;"),
                )
            )

            if rule["id"] not in registered_handlers:
                handle_delete_rule(target, rule["index"], rule["id"])
                registered_handlers.add(rule["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(ui.tags.tr(*[ui.tags.th(column) for column in columns])),
                ui.tags.tbody(*table_row),
                class_="rules-table",
            ),
            class_="d-flex flex-column w-100 mh-75 overflow-auto align-items-center",
        )

    def handle_delete_rule(target, index, rule_id):
        @reactive.effect
        @reactive.event(input[f"delete_{target}_rule_{index}"])
        def delete_rule_handler():
            delete_rule(session._parent.client, rule_id)
            trigger_update_rules.set(not trigger_update_rules())

    @reactive.effect
    @reactive.event(input.add_rule_button)
    def add_rule_modal():
        datasets = get_datasets_names(session._parent.client)
        modal = ui.modal(
            ui.div(
                ui.input_text("user_email", "User email"),
                ui.input_select(
                    "dataset_name",
                    "Dataset name",
                    datasets,
                    selected="",
                ),
                ui.input_radio_buttons(
                    "rule_type",
                    "Rule type",
                    {"approve": "Approve", "reject": "Reject"},
                ),
                ui.input_date("expires_at", "Expires at"),
                ui.input_action_button("add_rule", "Add Rule", class_="btn btn-primary mt-3"),
                class_="d-flex flex-column gap-2 py-3 justify-content-center align-items-center",
                style="width: 100",
            ),
            title=None,
            footer=None,
            size="l",
            easy_close=True,
        )
        ui.modal_show(modal)

    @reactive.effect
    @reactive.event(input.add_rule)
    def handle_add_rule():
        user_id = input.user_email() if input.user_email() else None
        dataset_id = input.dataset_name() if input.dataset_name() else None
        rule_type = input.rule_type()
        expires_date = input.expires_at()

        if user_id is None and dataset_id is None:
            ui.notification_show("Please provide either a user or a dataset", type="error")
            return

        try:
            add_rule(session._parent.client, user_id, dataset_id, rule_type, expires_date)
            trigger_update_rules.set(not trigger_update_rules())
        except ValueError as e:
            ui.notification_show(str(e), type="error")
            return

        ui.notification_show("Rule added successfully!", type="success")
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.apply_rules_button)
    def apply_rules_on_requests_handler():
        request_decisions.set(apply_rules_on_requests(session._parent.client))
        show_apply_decisions_page.set(True)

    @render.ui
    @reactive.event(trigger_change_decisions, show_apply_decisions_page)
    def apply_decisions_output():
        approve_requests = []
        reject_requests = []
        pending_requests = []
        if request_decisions() is not None:
            for request in request_decisions().values():
                if request["auto_decision"] == "approve":
                    approve_requests.append(request)
                elif request["auto_decision"] == "reject":
                    reject_requests.append(request)
                else:
                    pending_requests.append(request)

        return ui.div(
            ui.input_action_button(
                "back_button",
                arrow_left,
                class_="custom-button position-absolute z-1 p-0",
            ),
            ui.h1("Apply Decisions", class_="text-center my-5"),
            ui.div(
                ui.tooltip(
                    ui.input_action_button("apply_decisions_button", play_icon, class_="custom-button p-3"),
                    "Apply decisions",
                ),
                class_="d-flex flex-column gap-2 position-absolute top-0 end-0 z-1",
                style="margin: 48px 48px 0 0;",
            ),
            ui.div(
                ui.div(
                    ui.accordion(
                        make_decision_accordion_panel("approve", approve_requests),
                        make_decision_accordion_panel("reject", reject_requests),
                        make_decision_accordion_panel("pending", pending_requests),
                        open=True,
                        class_="approval-accordion d-flex flex-column w-100 h-100",
                    ),
                    style="width: 75%; max-height: 75vh; overflow-y: auto;",
                ),
                class_="d-flex w-100 h-100 align-items-center justify-content-center",
            ),
            class_="d-flex flex-column w-100 h-100",
        )

    @reactive.effect
    @reactive.event(input.back_button)
    def back_button_handler():
        show_apply_decisions_page.set(False)
        request_decisions.set(None)
        final_decisions.set({})
        final_approve_requests.set({})
        final_reject_requests.set({})

    def make_decision_accordion_panel(decision, requests):
        return ui.accordion_panel(decision.capitalize(), handle_decision_section(decision, requests))

    def handle_decision_section(decision, requests):
        if requests == []:
            return ui.div(
                ui.h5(f"There are no automatic {decision} requests.", class_="text-center my-4"),
                class_="d-flex flex-column w-100 h-100 align-items-center",
                style="background-color: #f3f4f6;",
            )

        table_row = []
        for request in requests:
            inspect_button = ui.input_action_button(
                f"inspect_request_{request['request_id']}",
                ui.div(
                    ui.span(search_icon, class_="table-icon-button"),
                    ui.span("Inspect"),
                    class_="d-flex justify-content-center align-items-center",
                ),
                class_="btn btn-primary btn-sm",
            )

            if request["request_id"] not in final_decisions():
                final_decisions()[request["request_id"]] = "pending"

            current_decision = final_decisions()[request["request_id"]]
            approve_button = ui.input_action_button(
                f"approve_button_{request['request_id']}",
                check_icon if current_decision != "approve" else check_icon_green,
                class_="custom-button p-2",
            )
            reject_button = ui.input_action_button(
                f"reject_button_{request['request_id']}",
                x_icon if current_decision != "reject" else x_icon_red,
                class_="custom-button p-2",
            )

            table_row.append(
                ui.tags.tr(
                    ui.tags.td(
                        approve_button,
                        reject_button,
                        class_="d-flex flex-row gap-4 align-items-center justify-content-center",
                        style="width: 200px;",
                    ),
                    ui.tags.td(request["description"], style="text-align: left;"),
                    ui.tags.td(inspect_button, style="text-align: right;"),
                )
            )

            request_id = request["request_id"]
            if request_id not in registered_handlers:
                handle_inspect_request(request_id)
                handle_approve_button(request_id)
                handle_reject_button(request_id)
                registered_handlers.add(request_id)

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Decision", style="width: 200px;"),
                        ui.tags.th("Request", style="text-align: left;"),
                        ui.tags.th(""),
                    )
                ),
                ui.tags.tbody(*table_row),
                class_="rules-table",
            ),
            class_="d-flex flex-column w-100 mh-75 overflow-auto align-items-center",
        )

    def handle_inspect_request(request_id):
        @reactive.effect
        @reactive.event(input[f"inspect_request_{request_id}"])
        def inspect_request_handler():
            current_request_id.set(request_id)
            toggle_inspect_modal.set(not toggle_inspect_modal())

    @reactive.effect
    @reactive.event(toggle_inspect_modal, current_request_id, ignore_init=True)
    def show_inspect_modal():
        current_request = request_decisions()[current_request_id()]

        request_time = current_request["request_time"].utc_timestamp
        formatted_request_date = datetime.fromtimestamp(request_time).strftime("%Y-%m-%d %H:%M")

        modal = ui.modal(
            ui.div(
                ui.h3(current_request["description"], class_="text-center pt-4 pb-3"),
                ui.div(
                    ui.p("This request belongs to the project:", style="margin: 0 8px 0 0;"),
                    ui.p(current_request["project_name"], style="font-weight: bold; margin-bottom: 0;"),
                    class_="info-container",
                ),
                ui.div(
                    ui.p("Id:", class_="info-title"),
                    ui.p(str(current_request["request_id"]), class_="mb-0"),
                    class_="info-container",
                ),
                ui.div(
                    ui.p("Requested by:", class_="info-title"),
                    ui.p(
                        f"{current_request['requesting_user_name']} ({current_request['requesting_user_email']})",
                        class_="mb-0",
                    ),
                    class_="info-container",
                ),
                ui.div(
                    ui.p("Requested at:", class_="info-title"),
                    ui.p(formatted_request_date, class_="mb-0"),
                    class_="info-container",
                ),
                ui.div(
                    ui.p("Datasets:", class_="info-title"),
                    ui.p(", ".join(current_request["dataset_names"]), class_="mb-0"),
                    class_="info-container",
                ),
                ui.p("Function code:", class_="info-title pb-1"),
                ui.div(ui.output_code("render_code"), style="max-height: 300px; overflow: auto;", class_="pb-4"),
            ),
            title=None,
            footer=None,
            size="l",
            easy_close=True,
        )
        ui.modal_show(modal)

    @render.code
    def render_code():
        current_request = request_decisions()[current_request_id()]
        return current_request["function_code"]

    def handle_approve_button(request_id):
        @reactive.effect
        @reactive.event(input[f"approve_button_{request_id}"])
        def approve_button_handler():
            final_decisions()[request_id] = "approve" if final_decisions()[request_id] != "approve" else "pending"

            trigger_change_decisions.set(not trigger_change_decisions())

    def handle_reject_button(request_id):
        @reactive.effect
        @reactive.event(input[f"reject_button_{request_id}"])
        def reject_button_handler():
            final_decisions()[request_id] = "reject" if final_decisions()[request_id] != "reject" else "pending"

            trigger_change_decisions.set(not trigger_change_decisions())

    @reactive.effect
    @reactive.event(input.apply_decisions_button)
    def handle_apply_decisions():
        temp_approve_requests = {}
        temp_reject_requests = {}

        items = []
        for request in request_decisions().values():
            request_id = request["request_id"]
            decision = final_decisions()[request_id]

            if decision == "approve":
                temp_approve_requests[request_id] = {
                    "project_id": request["project_id"],
                    "request_index": request["request_index"],
                }
                text_decision = ui.p("APPROVE", class_="text-success mb-0", style="font-weight: bold;")
            elif decision == "reject":
                temp_reject_requests[request_id] = {
                    "project_id": request["project_id"],
                    "request_index": request["request_index"],
                    "reason": "Rejected by governance rules.",
                }
                text_decision = ui.p("REJECT", class_="text-danger mb-0", style="font-weight: bold;")
            else:
                text_decision = ui.p("NO DECISION", class_="mb-0", style="font-weight: bold;")

            items.append(
                ui.div(
                    ui.p(f"- {request['description']}: ", style="margin: 0 8px 0 0;"),
                    text_decision,
                    class_="d-flex flex-row my-2",
                )
            )

        final_approve_requests.set(temp_approve_requests)
        final_reject_requests.set(temp_reject_requests)

        modal = ui.modal(
            ui.div(
                ui.h3("Apply Decisions", class_="text-center mb-3"),
                ui.p("Are you sure you want to apply the following decisions?"),
                *items,
                ui.div(
                    ui.input_action_button("confirm_apply_decisions", "Confirm", class_="btn btn-success"),
                    ui.input_action_button("cancel_apply_decisions", "Cancel", class_="btn btn-danger"),
                    class_="d-flex flex-row justify-content-center gap-5 mt-5",
                ),
                class_="px-3 pb-4 pt-2",
            ),
            title=None,
            footer=None,
            size="l",
            easy_close=True,
        )
        ui.modal_show(modal)

    @reactive.effect
    @reactive.event(input.confirm_apply_decisions)
    def confirm_apply_decisions():
        approve_multiple_requests(session._parent.client, final_approve_requests().values())
        reject_multiple_requests(session._parent.client, final_reject_requests().values())

        show_apply_decisions_page.set(False)
        ui.modal_remove()
        ui.notification_show("Decisions were successfully applied.", type="success")

    @reactive.effect
    @reactive.event(input.cancel_apply_decisions)
    def cancel_apply_decisions():
        ui.modal_remove()
