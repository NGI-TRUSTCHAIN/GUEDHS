from governance_ui.config import config
import requests
import structlog
from structlog.processors import TimeStamper, add_log_level


def set_static_info(_, __, event_dict):
    client = event_dict["client"]
    if client is not None:
        event_dict["custodian_id"] = client.logged_in_user
        event_dict["node_id"] = str(client.id)
        del event_dict["client"]
    event_dict["action_id"] = event_dict["action"].get("name")
    return event_dict


def transform_to_api_format(event_dict):
    key_transformer = {
        "custodian_id": "dataCustodianId",
        "node_id": "nodeId",
        "request_access_id": "accessId",
        "status": "status",
        "user_id": "dataUserId",
        "dataset_id": "datasetId",
    }
    return {key_transformer.get(key, key): value for key, value in event_dict.items() if key in key_transformer}


def send_to_blockchain(_, __, event_dict):
    endpoint = event_dict.get("action", {}).get("endpoint", "")
    url = f"{config.blockchain_api_url}{endpoint}"
    body = transform_to_api_format(event_dict)
    print(f"Sending to blockchain: {body}")
    print(f"URL: {url}")
    response = requests.post(
        url,
        json=body,
    )
    print(f"Response: {response}")
    return event_dict


structlog.configure(
    processors=[
        TimeStamper(fmt="iso"),
        add_log_level,
        set_static_info,
        send_to_blockchain,
        structlog.dev.ConsoleRenderer(),
    ]
)

logger = structlog.get_logger()
