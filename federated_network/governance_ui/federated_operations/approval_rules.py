from prisma import Prisma
import syft as sy
from datetime import datetime

db = Prisma()
db.connect()


def get_user_rules():
    rules = db.rule.find_many(where={"dataset_id": None})

    data = []
    for index, rule in enumerate(rules):
        data.append(
            {
                "index": index,
                "id": rule.id,
                "type": "Approve" if rule.type == "approve" else "Reject",
                "user_id": rule.user_id,
                "expires_at": rule.expires_at.strftime("%Y-%m-%d"),
            }
        )

    return data


def get_dataset_rules(client):
    rules = db.rule.find_many(where={"user_id": None})

    data = []
    for index, rule in enumerate(rules):
        dataset_name = client.datasets.get_by_id(sy.UID(rule.dataset_id)).name
        data.append(
            {
                "index": index,
                "id": rule.id,
                "type": "Approve" if rule.type == "approve" else "Reject",
                "dataset_name": dataset_name,
                "expires_at": rule.expires_at.strftime("%Y-%m-%d"),
            }
        )

    return data


def get_pair_rules(client):
    rules = db.rule.find_many(where={"NOT": [{"user_id": None}, {"dataset_id": None}]})

    data = []
    for index, rule in enumerate(rules):
        dataset_name = client.datasets.get_by_id(sy.UID(rule.dataset_id)).name
        data.append(
            {
                "index": index,
                "id": rule.id,
                "type": "Approve" if rule.type == "approve" else "Reject",
                "user_id": rule.user_id,
                "dataset_name": dataset_name,
                "expires_at": rule.expires_at.strftime("%Y-%m-%d"),
            }
        )

    return data


def delete_rule(rule_id):
    db.rule.delete(where={"id": rule_id})


def add_rule(client, user_id, dataset_id, rule_type, expires_date):
    expires_at = datetime(expires_date.year, expires_date.month, expires_date.day)

    if db.rule.find_first(
        where={"user_id": user_id, "dataset_id": dataset_id, "type": rule_type, "expires_at": expires_at}
    ):
        raise ValueError("Rule already exists")

    user_found = False
    if user_id:
        user_found = any(user.email == user_id for user in client.users)
        if not user_found:
            raise ValueError("User not found")

    db.rule.create(
        data={
            "type": rule_type,
            "user_id": user_id,
            "dataset_id": dataset_id,
            "expires_at": expires_at,
        }
    )
