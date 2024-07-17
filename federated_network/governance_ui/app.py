from shiny import App, ui
from governance_ui.server import server
from authlib.integrations.starlette_client import OAuth
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from governance_ui.config import config


oauth = OAuth()
oauth.register(
    name="fusionauth",
    client_id=config.fusionauth_client_id,
    client_secret=config.fusionauth_client_secret,
    authorize_url=f"{config.oauth_provider_auth_url}/oauth2/authorize",
    authorize_params=None,
    access_token_url=f"{config.oauth_provider_auth_url}/oauth2/token",
    access_token_params=None,
    refresh_token_url=None,
    authorize_state="secret-key",
    server_metadata_url=f"{config.oauth_provider_auth_url}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile offline_access",
    },
)


async def redirect_root(request):
    return RedirectResponse(url="/app")


shiny_app = App(ui.output_ui("main_page"), server)


async def login(request):
    redirect_uri = request.url_for("auth")
    return await oauth.fusionauth.authorize_redirect(request, redirect_uri)


async def auth(request):
    token = await oauth.fusionauth.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        request.session["user"] = user
    return RedirectResponse(url="/app")


async def logout(request):
    request.session.pop("user", None)
    return RedirectResponse(url="/app")


routes = [
    Route("/", endpoint=redirect_root),
    Mount("/app", shiny_app),
    Route("/login", endpoint=login),
    Route("/auth", endpoint=auth),
    Route("/logout", endpoint=logout),
]

app = Starlette(routes=routes)
app.add_middleware(SessionMiddleware, secret_key="secret-key")
