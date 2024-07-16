from shiny import module, reactive
from governance_ui.auth.login import login
from prisma import Prisma

db = Prisma()
db.connect()


@module.server
def auth_server(input, output, session, client):
    @reactive.effect
    @reactive.event(input.login, ignore_none=False)
    async def login_handler():
        try:
            user = session._parent.http_conn.session.get("user")
            if user:
                db_user = db.user.find_unique(where={"email": user.get("email")})
                r_client = login("localhost", "8081", db_user.email, db_user.pysyft_pwd)
                client.set(r_client)
            else:
                print("Redirecting to login")
                await session.send_custom_message("login", None)
        except Exception as e:
            print(f"Error: {e}")
            await session.send_custom_message("logout", None)
