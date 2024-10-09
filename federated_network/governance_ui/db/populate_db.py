from prisma import Prisma
from federated_network.governance_ui.config import config


def populate_db():
    db = Prisma()
    db.connect()

    user = db.user.find_many()

    if not user:
        print("Populating db with default user")
        db.user.create(
            data={
                "name": "info",
                "email": config.pysyft_root_user_email,
                "pysyft_pwd": config.pysyft_root_user_password,
            }
        )

    db.disconnect()


if __name__ == "__main__":
    populate_db()
