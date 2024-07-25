from governance_ui.logs import get_from_blockchain
from datetime import datetime


def get_audit_logs(filters):
    endpoint = "/audit-logs/all-operations"
    logs = get_from_blockchain(endpoint=endpoint)
    filtered_logs = []

    def convert_timestamp(timestamp):
        parts = timestamp.split()
        return " ".join(parts[:5])

    for action_type in filters:
        if action_type in logs:
            for log in logs[action_type]:
                filtered_logs.append(
                    {
                        "action_type": action_type,
                        "action": log["action"][1:],
                        "timestamp": convert_timestamp(log["timestamp"]),
                        "dataCustodianUUID": log["dataCustodianUUID"],
                        "json": log,
                    }
                )

    # Sort logs by timestamp
    filtered_logs.sort(key=lambda x: datetime.strptime(x["timestamp"], "%a %b %d %Y %H:%M:%S"), reverse=True)

    # Add index to logs
    for index, log in enumerate(filtered_logs):
        log["index"] = index

    return filtered_logs
