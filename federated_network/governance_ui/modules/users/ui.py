from shiny import module, ui
from pathlib import Path


@module.ui
def list_users_ui():
    return ui.page_fluid(
        ui.include_css(Path(__file__).parent / "../../styles.css"),
        ui.output_table("list_users_page"),
        class_="d-flex flex-row h-100 gap-5 px-3 align-items-center justify-content-center",
    )


@module.ui
def create_user_ui():
    return ui.page_fluid(
        ui.h1("Create User", class_="text-center my-5"),
        ui.div(
            ui.input_text("user_name", "* Name"),
            ui.input_text("user_email", "* Email"),
            ui.input_select(
                "user_role",
                "* Role",
                {
                    "admin": "Admin",
                    "data_scientist": "Data Scientist",
                },
                selected="data_scientist",
            ),
            class_="d-flex flex-column my-3 gap-3 justify-content-center align-items-center",
        ),
        ui.div(
            ui.div(
                ui.input_action_button("create_user", "Create User", class_="btn btn-primary w-100"),
                style="width: 240px;",
            ),
            class_="d-flex mt-5 justify-content-center align-items-center",
        ),
        class_="d-flex flex-column w-100 h-100",
    )
