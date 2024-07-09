from shiny import module, reactive
from shiny_validate import InputValidator, check
from governance_ui.auth.login import login


@module.server
def login_server(input, output, session, login_status):
    @reactive.effect
    @reactive.event(input.login)
    def handle_login():
        login_validator = InputValidator()
        login_validator.enable()
        login_validator.add_rule("url", check.required())
        login_validator.add_rule("port", check.required())
        login_validator.add_rule("email", check.required())
        login_validator.add_rule("email", check.email())
        login_validator.add_rule("password", check.required())

        if login_validator.is_valid():
            client = login(input.url(), input.port(), input.email(), input.password())
            if client:
                login_status.set(True)
                session._parent.client = client
