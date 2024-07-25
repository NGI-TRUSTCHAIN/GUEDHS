from governance_ui.actions import PySyftActions
from syft.service.user.user import UserCreate
from syft.service.user.user_roles import ServiceRole
from governance_ui.logs import logger
import secrets
from fusionauth.fusionauth_client import FusionAuthClient
from governance_ui.config import config
from prisma import Prisma

db = Prisma()
db.connect()


def get_users(client):
    logger.info("Listing data users", client=client, action=PySyftActions.LIST_USERS.value)

    data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.name,
            "role_value": user.role.value,
        }
        for user in client.users
    ]

    # Order by highest role value
    data = sorted(data, key=lambda x: x["role_value"], reverse=True)

    return data


def block_user(client, user_id):
    for user in client.users:
        if user.id == user_id:
            logger.info(
                "Blocking data scientist user",
                client=client,
                action=PySyftActions.DELETE_USER.value,
                user_id=user.email,
            )
            user.update(role="NONE")
            break


def unblock_user(client, user_id):
    for user in client.users:
        if user.id == user_id:
            logger.info(
                "Unblocking data scientist user",
                client=client,
                action=PySyftActions.CREATE_USER.value,
                user_id=user.email,
            )
            user.update(role="DATA_SCIENTIST")
            break


def create_data_scientist(client, user_name, user_email):
    logger.info(
        "Creating data scientist user",
        client=client,
        action=PySyftActions.CREATE_USER.value,
        user_id=user_email,
    )

    password = secrets.token_hex(8)

    client.register(
        name=user_name,
        email=user_email,
        password=password,
        password_verify=password,
    )

    return password


def create_admin(client, user_name, user_email):
    logger.info(
        "Creating admin user",
        client=client,
        action=PySyftActions.CREATE_USER.value,
        user_id=user_email,
    )

    pysyft_pwd = secrets.token_hex(8)

    new_user = UserCreate(
        name=user_name,
        email=user_email,
        password=pysyft_pwd,
        password_verify=pysyft_pwd,
        created_by=client.credentials,
        role=ServiceRole.ADMIN,
    )

    client.connection.register(new_user=new_user)

    db.user.create(data={"name": user_name, "email": user_email, "pysyft_pwd": pysyft_pwd})

    fusionauth_pwd = secrets.token_hex(8)

    fusionauth_client = FusionAuthClient(config.fusionauth_api_key, config.oauth_provider_auth_url)

    user_request = {
        "sendSetPasswordEmail": False,
        "skipVerification": True,
        "user": {
            "email": user_email,
            "password": fusionauth_pwd,
        },
    }

    response = fusionauth_client.create_user(user_request, None)

    if response.was_successful():
        print("User created successfully!")
    else:
        print("User creation failed!")

    return fusionauth_pwd
