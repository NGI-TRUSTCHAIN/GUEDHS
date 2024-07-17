from shiny import module, ui
from governance_ui.config import config


@module.ui
def auth_ui():
    return ui.page_fluid(
        ui.input_action_button("login", "", class_="d-none"),
        ui.tags.script(
            f"""
                $(function() {{
                    Shiny.addCustomMessageHandler("login", function(message) {{
                        window.location.replace("http://{config.oauth_provider_app_url}/login");
                    }});
                }});
            """
        ),
        ui.tags.script(
            f"""
                $(function() {{
                    Shiny.addCustomMessageHandler("logout", function(message) {{
                        window.location.replace("http://{config.oauth_provider_auth_url}/oauth2/logout?client_id={config.fusionauth_client_id}");
                    }});
                }});
            """
        ),
        class_="pt-5 d-flex flex-column align-items-center",
        style="background-color: #f3f4f6 !important; height: 100vh;",
    )
