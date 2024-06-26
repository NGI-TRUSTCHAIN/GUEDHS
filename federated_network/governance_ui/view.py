from shiny import ui
from pathlib import Path

css_path = Path(__file__).parent / "styles.css"
ui.include_css(css_path)

login_ui = ui.page_fluid(
    ui.div(
        ui.h1("GUEHDS Portal", class_="text-center mb-4"),
        ui.h2("Tenant Login", class_="text-center mb-4")
    ),
    ui.div(
        ui.div(
            ui.input_text("url", "URL"),
            ui.input_text("port", "Port"),
            ui.input_text("email", "Email"),
            ui.input_password("password", "Password"),
            ui.input_action_button("login", "Login", class_="btn btn-primary mt-3"),
            class_="p-5",
            style="background-color: #e5e7eb; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
        ),
        class_="mt-3 row justify-content-center"
    ),
    class_="pt-5 d-flex flex-column align-items-center",
    style="background-color: #f3f4f6 !important; height: 100vh;"
)

datasets_ui = ui.page_fluid(
    ui.div(
        ui.div(
            ui.h1("Datasets", class_="text-center mb-5"),
            ui.output_ui("datasets_content")
        ),
        class_="container mt-5 d-flex flex-column align-items-center"
    )
)

create_dataset_ui = ui.page_fluid(
    ui.div(
        ui.div(
            ui.h2("Create Dataset"),
            ui.input_text("dataset_name", "Dataset Name"),
            ui.input_text("dataset_description", "Dataset Description"),
            ui.input_file("dataset_file", "Dataset File"),
            ui.input_action_button("change", "Create Dataset", class_="btn btn-primary mt-3"),
            class_="mt-4"
        ),
        class_="container mt-5 d-flex flex-column align-items-center"
    )
)

dashboards_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("GUEHDS Portal", class_="text-center mt-4 mb-3"),
        ui.input_action_button("show_datasets_button", "Datasets", class_="btn btn-primary"),
        ui.input_action_button("create_dataset_button", "Create Dataset", class_="btn btn-primary"),
        style="background-color: #e5e7eb; height: 100vh; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
    ),
    ui.div(
        ui.output_ui("content_ui"),
    ),
    style="background-color: #f3f4f6 !important; height: 100vh;"
)

