from shiny import module, ui


@module.ui
def auth_ui():
    return ui.page_fluid(
        ui.input_action_button("login", "", class_="d-none"),
        ui.tags.script(
            """
                $(function() {
                    Shiny.addCustomMessageHandler("login", function(message) {
                        window.location.replace("http://guehds.local.promptly.health:8000/login");
                    });
                });
                """
        ),
        ui.tags.script(
            """
                $(function() {
                    Shiny.addCustomMessageHandler("logout", function(message) {
                        window.location.replace("http://localhost:9011/oauth2/logout?client_id=228a7299-ae57-4fab-b5dd-c595ba5709df");
                    });
                });
                """
        ),
        class_="pt-5 d-flex flex-column align-items-center",
        style="background-color: #f3f4f6 !important; height: 100vh;",
    )
