from shiny import module, ui


@module.ui
def datasets_ui():
    return ui.page_fluid(
        ui.div(
            ui.card(
                ui.h1("Datasets", class_="text-center mt-5 mb-3"),
                ui.div(
                    ui.output_ui("datasets_left"),
                    style="height: 600px; width: 100%; overflow-y: auto; overflow-x: hidden;",
                ),
                height="90%",
            ),
            class_="w-50 h-100 d-flex flex-column justify-content-center",
        ),
        ui.div(
            ui.card(ui.output_ui("dataset_content"), height="90%"),
            class_="w-50 h-100 d-flex flex-column justify-content-center",
        ),
        class_="d-flex flex-row h-100 gap-5 px-3",
    )


@module.ui
def register_dataset_ui():
    return ui.page_fluid(
        ui.div(
            ui.h1("Register Dataset", class_="text-center my-5"),
            ui.div(
                ui.div(
                    ui.h4("Dataset Info:"),
                    ui.input_text("dataset_name", "Name"),
                    ui.input_text("dataset_description", "Description"),
                ),
                ui.div(
                    ui.h4("Asset Info:"),
                    ui.input_text("asset_name", "Name"),
                    ui.input_text("asset_description", "Description"),
                    ui.div(
                        ui.input_text("data_url", "Dataset URL"),
                        ui.p("or", class_="mt-4"),
                        ui.input_file("data_file", "Dataset File"),
                        class_="d-flex flex-row gap-5",
                    ),
                    ui.div(
                        ui.input_text("mock_url", "Mock URL (Optional)"),
                        ui.p("or", class_="mt-4"),
                        ui.input_file("mock_file", "Mock File (Optional)"),
                        class_="d-flex flex-row gap-5",
                    ),
                    class_="d-flex flex-column justify-content-center mt-5",
                ),
                ui.input_action_button("register_dataset", "Register Dataset", class_="btn btn-primary mt-3 w-50"),
            ),
            class_="d-flex flex-column w-100 h-100 align-items-center",
        )
    )
