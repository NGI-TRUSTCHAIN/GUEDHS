from prisma import Prisma
import syft as sy
from datetime import datetime
from governance_ui.federated_operations.projects import execute_code, approve_request, reject_request

db = Prisma()
db.connect()


def get_user_rules(client):
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

    if expires_at < datetime.now():
        raise ValueError("Invalid expiration date!")

    repeated_rule = db.rule.find_first(where={"user_id": user_id, "dataset_id": dataset_id, "expires_at": expires_at})
    if repeated_rule:
        if repeated_rule.type == rule_type:
            raise ValueError("Rule already exists!")
        else:
            raise ValueError("Same rule with different type already exists!")

    user_found = False
    if user_id:
        user_found = any(user.email == user_id for user in client.users)
        if not user_found:
            raise ValueError("User not found!")

    db.rule.create(
        data={
            "type": rule_type,
            "user_id": user_id,
            "dataset_id": dataset_id,
            "expires_at": expires_at,
        }
    )


def apply_rules(client):
    projects = client.projects.get_all()
    datasets = {dataset.asset_list[0].id: str(dataset.id) for dataset in client.datasets.get_all()}
    results = {
        "approved": 0,
        "rejected": 0,
        "pending": 0,
    }

    for project in projects:
        print("Checking project:", project.name)

        if not project.pending_requests:
            print("No pending requests for project:", project.name)
            continue

        project_id = project.id
        for request_index, request in enumerate(project.requests):
            user_id = request.requesting_user_email
            func = request.code

            approve_set = set()
            for asset in func.assets:
                dataset_id = datasets[asset.id]
                rule = check_rule(user_id, dataset_id)
                approve_set.add(rule) if rule is not None else None

            if len(approve_set) == 1:
                if True in approve_set:
                    print("Will approve request!")
                    _, real_result = execute_code(client, project_id, request_index)
                    approve_request(client, project_id, request_index, real_result)
                    results["approved"] += 1
                else:
                    print("Will reject request!")
                    reject_request(client, project_id, request_index, "Rejected by rule!")
                    results["rejected"] += 1
            else:
                print("Inconsistent rules found, let supervisor decide!")
                results["pending"] += 1

    return results


def check_rule(user_id, dataset_id):
    reject_match = db.rule.find_first(
        where={
            "OR": [
                {"user_id": user_id, "dataset_id": dataset_id, "type": "reject"},
                {"user_id": None, "dataset_id": dataset_id, "type": "reject"},
                {"user_id": user_id, "dataset_id": None, "type": "reject"},
            ]
        }
    )
    approve_match = db.rule.find_first(
        where={
            "OR": [
                {"user_id": user_id, "dataset_id": dataset_id, "type": "approve"},
                {"user_id": None, "dataset_id": dataset_id, "type": "approve"},
                {"user_id": user_id, "dataset_id": None, "type": "approve"},
            ]
        }
    )

    if not (approve_match or reject_match):
        return None

    if not (approve_match and reject_match):
        return bool(approve_match)

    approve_match_score = bool(approve_match.user_id) + bool(approve_match.dataset_id)
    reject_match_score = bool(reject_match.user_id) + bool(reject_match.dataset_id)

    if approve_match_score < reject_match_score:
        return False
    elif approve_match_score > reject_match_score:
        return True
    else:
        return None
