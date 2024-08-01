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

    sections = {
        "user_rules": {
            "target": "user",
            "fields": ["type", "user_id", "expires_at"],
            "columns": ["Type", "User", "Expires At"],
            "trigger": trigger_update_user_rules,
            "get_rules_func": get_user_rules,
        },
        "dataset_rules": {
            "target": "dataset",
            "fields": ["type", "dataset_name", "expires_at"],
            "columns": ["Type", "Dataset", "Expires At"],
            "trigger": trigger_update_dataset_rules,
            "get_rules_func": get_dataset_rules,
        },
        "pair_rules": {
            "target": "pair",
            "fields": ["type", "user_id", "dataset_name", "expires_at"],
            "columns": ["Type", "User", "Dataset", "Expires At"],
            "trigger": trigger_update_pair_rules,
            "get_rules_func": get_pair_rules,
        },
    }

    @render.ui
    @reactive.event(trigger_update_user_rules)
    def user_rules_section():
        return handle_rule_section(
            sections["user_rules"]["target"],
            sections["user_rules"]["fields"],
            sections["user_rules"]["columns"],
            sections["user_rules"]["trigger"],
            sections["user_rules"]["get_rules_func"],
        )

    @render.ui
    @reactive.event(trigger_update_dataset_rules)
    def dataset_rules_section():
        return handle_rule_section(
            sections["dataset_rules"]["target"],
            sections["dataset_rules"]["fields"],
            sections["dataset_rules"]["columns"],
            sections["dataset_rules"]["trigger"],
            sections["dataset_rules"]["get_rules_func"],
        )

    @render.ui
    @reactive.event(trigger_update_pair_rules)
    def pair_rules_section():
        return handle_rule_section(
            sections["pair_rules"]["target"],
            sections["pair_rules"]["fields"],
            sections["pair_rules"]["columns"],
            sections["pair_rules"]["trigger"],
            sections["pair_rules"]["get_rules_func"],
        )

    def handle_rule_section(target, fields, columns, trigger, get_rules_func):
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
                handle_delete_rule(target, rule["index"], rule["id"], trigger)
                registered_handlers.add(rule["id"])

        return ui.div(
            ui.tags.table(
                ui.tags.thead(ui.tags.tr(*[ui.tags.th(column) for column in columns])),
                ui.tags.tbody(*table_row),
                class_="rules-table",
            ),
            class_="d-flex flex-column w-100 mh-75 overflow-auto align-items-center",
        )

    def handle_delete_rule(target, index, rule_id, trigger):
        @reactive.effect
        @reactive.event(input[f"delete_{target}_rule_{index}"])
        def delete_rule_handler():
            delete_rule(rule_id)
            trigger.set(not trigger())

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
