from prisma import Prisma
import syft as sy
from datetime import datetime
from governance_ui.actions import PySyftActions
from governance_ui.logs import logger
import uuid

db = Prisma()
db.connect()


def get_user_rules(client):
    logger.info(
        "Listing data operation rules",
        client=client,
        action=PySyftActions.LIST_DATA_OP_RULES.value,
    )

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
    logger.info(
        "Listing data operation rules",
        client=client,
        action=PySyftActions.LIST_DATA_OP_RULES.value,
    )

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
    logger.info(
        "Listing data operation rules",
        client=client,
        action=PySyftActions.LIST_DATA_OP_RULES.value,
    )

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


def delete_rule(client, rule_id):
    logger.info(
        "Removing data operation rule",
        client=client,
        action=PySyftActions.DELETE_DATA_OP_RULE.value,
        rule_id=rule_id,
    )

    db.rule.delete(where={"id": rule_id})


def add_rule(client, user_id, dataset_id, rule_type, expires_date):
    rule_id = str(uuid.uuid4())

    logger.info(
        "Creating data operation rule",
        client=client,
        action=PySyftActions.CREATE_DATA_OP_RULE.value,
        rule_id=rule_id,
    )

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
            "id": rule_id,
            "type": rule_type,
            "user_id": user_id,
            "dataset_id": dataset_id,
            "expires_at": expires_at,
        }
    )


def apply_rules_on_requests(client):
    datasets = {}
    logger.info("Listing datasets", client=client, action=PySyftActions.LIST_DATASETS.value)
    for dataset in client.datasets.get_all():
        logger.info(
            "Inspecting dataset",
            client=client,
            action=PySyftActions.INSPECT_DATASET.value,
            dataset_id=dataset.id,
        )
        datasets[dataset.asset_list[0].id] = (str(dataset.id), dataset.name)

    request_decisions = {}
    logger.info(
        "Listing access requests",
        client=client,
        action=PySyftActions.LIST_ACCESS_REQUESTS.value,
    )
    for project in client.projects.get_all():
        if not project.pending_requests:
            continue

        for request_index, request in enumerate(project.requests):
            user_id = request.requesting_user_email
            approve_set = set()
            request_dataset_names = []
            datasets_ids = []
            for asset in request.code.assets:
                dataset_id = datasets[asset.id][0]
                datasets_ids.append(dataset_id)
                request_dataset_names.append(datasets[asset.id][1])
                rule = check_rule(user_id, dataset_id)
                approve_set.add(rule) if rule is not None else None

            logger.info(
                "Inspecting access request",
                client=client,
                action=PySyftActions.INSPECT_ACCESS_REQUEST.value,
                user_id=request.requesting_user_email,
                dataset_id=", ".join(datasets_ids),
                status=request.status.name,
                request_access_id=str(request.id),
            )

            decision = {
                "project_id": project.id,
                "project_name": project.name,
                "request_id": request.id,
                "request_index": request_index,
                "description": "Request to approve " + request.code.service_func_name,
                "request_time": request.request_time,
                "requesting_user_name": request.requesting_user_name,
                "requesting_user_email": request.requesting_user_email,
                "function_code": request.code.raw_code,
                "dataset_names": request_dataset_names,
                "auto_decision": "pending",
            }

            if len(approve_set) == 1:
                decision["auto_decision"] = "approve" if True in approve_set else "reject"
            request_decisions[request.id] = decision

    return request_decisions


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
