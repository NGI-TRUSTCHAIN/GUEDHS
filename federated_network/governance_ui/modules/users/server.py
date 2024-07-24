from shiny import module, render, ui, reactive
from shiny_validate import InputValidator, check
from governance_ui.federated_operations.users import (
    get_users,
    block_user,
    unblock_user,
    create_data_scientist,
    create_admin,
)
from governance_ui.icons import block_icon, undo_icon


@module.server
def users_server(input, output, session, users_button):
    users = reactive.Value([])
    registered_handlers = set()
    user_updated = reactive.Value(False)

    @render.ui
    @reactive.event(users_button, user_updated, ignore_none=False)
    def list_users_page():
        users.set(get_users(session._parent.client))

        if user_updated():
            user_updated.set(False)

        if len(users()) > 0:
            return ui.output_ui("users_table")
        else:
            return ui.h4("No users found", class_="text-center")

    @render.ui
    def users_table():
        table_rows = []

        for user in users():
            if user["role"] == "ADMIN":
                mod_button = None
            elif user["role"] != "NONE":
                mod_button = ui.input_action_button(
                    f"block_user_{user['id']}",
                    ui.div(
                        ui.span(block_icon, class_="table-icon-button"),
                        ui.span("Block"),
                        class_="d-flex justify-content-center align-items-center",
                    ),
                    class_="btn btn-sm btn-danger",
                )
            else:
                mod_button = ui.input_action_button(
                    f"unblock_user_{user['id']}",
                    ui.div(
                        ui.span(undo_icon, class_="table-icon-button"),
                        ui.span("Unblock"),
                        class_="d-flex justify-content-center align-items-center",
                    ),
                    class_="btn btn-sm btn-success",
                )

            table_rows.append(
                ui.tags.tr(
                    ui.tags.td(user["name"]),
                    ui.tags.td(user["email"]),
                    ui.tags.td(user["role"]),
                    ui.tags.td(mod_button),
                )
            )

            if user["id"] not in registered_handlers:
                registered_handlers.add(user["id"])
                handle_block_user(user["id"])
                handle_unblock_user(user["id"])

        return ui.div(
            ui.h1("User Management", class_="text-center my-5"),
            ui.div(
                ui.tags.table(
                    ui.tags.thead(
                        ui.tags.tr(
                            ui.tags.th("Name"),
                            ui.tags.th("Email"),
                            ui.tags.th("Role"),
                            ui.tags.th(""),
                        )
                    ),
                    ui.tags.tbody(*table_rows),
                    style="width: 100%; !important;",
                    class_="bigger-table",
                ),
                class_="w-auto mw-50 h-75 overflow-auto",
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )

    def handle_block_user(user_id):
        @reactive.effect
        @reactive.event(input[f"block_user_{user_id}"])
        def block_handler():
            block_user(session._parent.client, user_id)
            user_updated.set(True)

    def handle_unblock_user(user_id):
        @reactive.effect
        @reactive.event(input[f"unblock_user_{user_id}"])
        def unblock_handler():
            unblock_user(session._parent.client, user_id)
            user_updated.set(True)

    @reactive.effect
    @reactive.event(input.create_user)
    def handle_create_user():
        input_validator = InputValidator()
        input_validator.enable()
        input_validator.add_rule("user_name", check.required())
        input_validator.add_rule("user_email", check.required())
        input_validator.add_rule("user_email", check.email())

        if input_validator.is_valid():
            user_name = input.user_name()
            user_email = input.user_email()
            user_role = input.user_role()
            fusionauth_pwd = None
            pysyft_pwd = None

            if user_role == "admin":
                fusionauth_pwd = create_admin(session._parent.client, user_name, user_email)
            else:
                pysyft_pwd = create_data_scientist(session._parent.client, user_name, user_email)

            if fusionauth_pwd or pysyft_pwd:
                modal = ui.modal(
                    ui.div(
                        ui.p(
                            f"Copy the {'Portal ' if fusionauth_pwd else 'PySyft '}\
                              Password below and send it to the user:",
                            style="font-size: 18px;",
                        ),
                        ui.div(
                            ui.p(f"{fusionauth_pwd or pysyft_pwd}", style="font-size: 18px; font-weight: bold;"),
                            class_="text-center pt-3 pb-5",
                        ),
                    ),
                    title="User created successfully!",
                    footer=None,
                    easy_close=True,
                )
                ui.modal_show(modal)

            user_updated.set(True)
