import structlog
from structlog.processors import TimeStamper, add_log_level, KeyValueRenderer

def set_static_info(_, __, event_dict):
    client = event_dict["client"]
    if client is not None:
        event_dict["custodian_id"] = client.logged_in_user
        event_dict["node_id"] = str(client.id)
        del event_dict["client"]
    return event_dict

structlog.configure(
    processors=[
        TimeStamper(fmt="iso"),
        add_log_level,
        set_static_info,
        structlog.dev.ConsoleRenderer(),
    ]
)

logger = structlog.get_logger()
