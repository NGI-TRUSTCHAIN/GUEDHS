from shiny import module, ui


@module.ui
def auth_ui():
    return ui.output_ui("login_handler")
