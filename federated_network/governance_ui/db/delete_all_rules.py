from prisma import Prisma


def delete_all_rules():
    db = Prisma()
    db.connect()

    print("Deleting all rules")
    db.rule.delete_many()

    db.disconnect()


if __name__ == "__main__":
    delete_all_rules()
