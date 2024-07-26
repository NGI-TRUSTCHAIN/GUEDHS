from prisma import Prisma


def populate_db():
    db = Prisma()
    db.connect()

    db.user.create(data={"name": "info", "email": "info@openmined.org", "pysyft_pwd": "changethis"})

    # user = db.user.find_many()
    # print(user)

    db.disconnect()


if __name__ == "__main__":
    populate_db()
