from shiny import App, ui
from governance_ui.server import server

# Initialize the app with the main UI component and the server logic
app = App(ui.output_ui("main_page"), server)
