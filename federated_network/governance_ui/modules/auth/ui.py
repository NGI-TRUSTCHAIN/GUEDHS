from shiny import module, ui


@module.ui
def login_ui():
    return ui.page_fluid(
        ui.div(
            ui.h1("GUEHDS Portal", class_="text-center mb-4"),
            ui.h2("Tenant Login", class_="text-center mb-4"),
        ),
        ui.div(
            ui.div(
                ui.input_text("url", "URL"),
                ui.input_text("port", "Port"),
                ui.input_text("email", "Email"),
                ui.input_password("password", "Password"),
                ui.input_action_button("login", "Login", class_="btn btn-primary mt-3"),
                class_="p-5",
                style="background-color: #e5e7eb; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);",
            ),
            class_="mt-3 row justify-content-center",
        ),
        class_="pt-5 d-flex flex-column align-items-center",
        style="background-color: #f3f4f6 !important; height: 100vh;",
    )
