from shiny import module, reactive, render, ui
from governance_ui.auth.login import login
from prisma import Prisma

db = Prisma()
db.connect()


@module.server
def auth_server(input, output, session, client):
    @render.ui
    def login_handler():
        try:
            user = session._parent.http_conn.session.get("user")
            if user:
                db_user = db.user.find_unique(where={"email": user.get("email")})
                r_client = login("localhost", "8081", db_user.email, db_user.pysyft_pwd)
                client.set(r_client)
                return None
            else:
                print("Redirecting to login")
                return render_login
        except Exception as e:
            print(f"Error: {e}")
            return render_logout

    @render.ui
    def render_login():
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
            class_="pt-5 d-flex flex-column align-items-center",
            style="background-color: #f3f4f6 !important; height: 100vh;",
        )

    @reactive.effect
    @reactive.event(input.login, ignore_none=False)
    async def handle_login():
        await session.send_custom_message("login", None)

    @render.ui
    def render_logout():
        return ui.page_fluid(
            ui.input_action_button("logout", "", class_="d-none"),
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

    @reactive.effect
    @reactive.event(input.logout, ignore_none=False)
    async def handle_logout():
        await session.send_custom_message("logout", None)
