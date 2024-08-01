from shiny import module, render, ui, reactive
from governance_ui.federated_operations.approval_rules import (
    get_user_rules,
    get_dataset_rules,
    get_pair_rules,
    delete_rule,
    add_rule,
)
from governance_ui.federated_operations.datasets import get_datasets_names
from governance_ui.icons import trash_icon


@module.server
def approval_rules_server(input, output, session):
    trigger_update_user_rules = reactive.Value(True)
    trigger_update_dataset_rules = reactive.Value(True)
    trigger_update_pair_rules = reactive.Value(True)
    registered_handlers = set()

    @render.ui
    @reactive.event(trigger_update_user_rules)
    def user_rules_section():
        user_rules = get_user_rules()

        if user_rules == []:
            return ui.div(
                ui.h5("No user rules available.", class_="text-center my-4"),
                class_="d-flex flex-column w-100 h-100 align-items-center",
                style="background-color: #f3f4f6;",
            )

        sorted_rules = sorted(user_rules, key=lambda x: x["expires_at"])

        table_row = []
        for rule in sorted_rules:
            delete_rule_button = ui.input_action_button(
                f"delete_user_rule_{rule['index']}",
                trash_icon,
                class_="custom-button",
            )

            table_row.append(
                ui.tags.tr(
                    ui.tags.td(rule["type"]),
                    ui.tags.td(rule["user_id"]),
                    ui.tags.td(rule["expires_at"]),
                    ui.tags.td(delete_rule_button, style="text-align: right;"),
                )
            )

            if rule["id"] not in registered_handlers:
                handle_delete_user_rule(rule["index"], rule["id"])
                registered_handlers.add(rule["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Type"),
                        ui.tags.th("User"),
                        ui.tags.th("Expires At"),
                        ui.tags.th(""),
                    )
                ),
                ui.tags.tbody(*table_row),
                class_="rules-table",
            ),
            class_="d-flex flex-column w-100 mh-75 overflow-auto align-items-center",
        )

    def handle_delete_user_rule(index, rule_id):
        @reactive.effect
        @reactive.event(input[f"delete_user_rule_{index}"])
        def delete_user_rule():
            delete_rule(rule_id)
            trigger_update_user_rules.set(not trigger_update_user_rules())

    @render.ui
    @reactive.event(trigger_update_dataset_rules)
    def dataset_rules_section():
        dataset_rules = get_dataset_rules(session._parent.client)

        if dataset_rules == []:
            return ui.div(
                ui.h5("No dataset rules available.", class_="text-center my-4"),
                class_="d-flex flex-column w-100 h-100 align-items-center",
                style="background-color: #f3f4f6;",
            )

        sorted_rules = sorted(dataset_rules, key=lambda x: x["expires_at"])

        table_row = []
        for rule in sorted_rules:
            delete_rule_button = ui.input_action_button(
                f"delete_dataset_rule_{rule['index']}",
                trash_icon,
                class_="custom-button",
            )

            table_row.append(
                ui.tags.tr(
                    ui.tags.td(rule["type"]),
                    ui.tags.td(rule["dataset_name"]),
                    ui.tags.td(rule["expires_at"]),
                    ui.tags.td(delete_rule_button, style="text-align: right;"),
                )
            )

            if rule["id"] not in registered_handlers:
                handle_delete_dataset_rule(rule["index"], rule["id"])
                registered_handlers.add(rule["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Type"),
                        ui.tags.th("Dataset"),
                        ui.tags.th("Expires At"),
                        ui.tags.th(""),
                    )
                ),
                ui.tags.tbody(*table_row),
                class_="rules-table",
            ),
            class_="d-flex flex-column w-100 mh-75 overflow-auto align-items-center",
        )

    def handle_delete_dataset_rule(index, rule_id):
        @reactive.effect
        @reactive.event(input[f"delete_dataset_rule_{index}"])
        def delete_dataset_rule():
            delete_rule(rule_id)
            trigger_update_dataset_rules.set(not trigger_update_dataset_rules())

    @render.ui
    @reactive.event(trigger_update_pair_rules)
    def pair_rules_section():
        pair_rules = get_pair_rules(session._parent.client)

        if pair_rules == []:
            return ui.div(
                ui.h5("No pair rules available.", class_="text-center my-4"),
                class_="d-flex flex-column w-100 h-100 align-items-center",
                style="background-color: #f3f4f6;",
            )

        sorted_rules = sorted(pair_rules, key=lambda x: x["expires_at"])

        table_row = []
        for rule in sorted_rules:
            delete_rule_button = ui.input_action_button(
                f"delete_pair_rule_{rule['index']}",
                trash_icon,
                class_="custom-button",
            )

            table_row.append(
                ui.tags.tr(
                    ui.tags.td(rule["type"]),
                    ui.tags.td(rule["user_id"]),
                    ui.tags.td(rule["dataset_name"]),
                    ui.tags.td(rule["expires_at"]),
                    ui.tags.td(delete_rule_button, style="text-align: right;"),
                )
            )

            if rule["id"] not in registered_handlers:
                handle_delete_pair_rule(rule["index"], rule["id"])
                registered_handlers.add(rule["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th("Type"),
                        ui.tags.th("User"),
                        ui.tags.th("Dataset"),
                        ui.tags.th("Expires At"),
                        ui.tags.th(""),
                    )
                ),
                ui.tags.tbody(*table_row),
                class_="rules-table",
            ),
            class_="d-flex flex-column w-100 mh-75 overflow-auto align-items-center",
        )

    def handle_delete_pair_rule(index, rule_id):
        @reactive.effect
        @reactive.event(input[f"delete_pair_rule_{index}"])
        def delete_pair_rule():
            delete_rule(rule_id)
            trigger_update_pair_rules.set(not trigger_update_pair_rules())

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

            if user_id and dataset_id:
                trigger_update_pair_rules.set(not trigger_update_pair_rules())
            elif user_id:
                trigger_update_user_rules.set(not trigger_update_user_rules())
            else:
                trigger_update_dataset_rules.set(not trigger_update_dataset_rules())
        except ValueError as e:
            ui.notification_show(str(e), type="error")
            return

        ui.modal_remove()
