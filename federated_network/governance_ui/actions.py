import enum


class PySyftActions(enum.Enum):
    # Dataset Management
    LIST_DATASETS = {"name": "list_datasets", "endpoint": "/datasets/list-datasets"}
    INSPECT_DATASET = {
        "name": "inspect_dataset",
        "endpoint": "/datasets/inspect-dataset",
    }
    CREATE_DATASET = {"name": "create_dataset", "endpoint": "/datasets/create-dataset"}

    # Access Request Management
    LIST_ACCESS_REQUESTS = {
        "name": "list_access_requests",
        "endpoint": "/access-request/list-access",
    }
    INSPECT_ACCESS_REQUEST = {
        "name": "inspect_access_request",
        "endpoint": "/access-request/inspect-access",
    }
    ACCEPT_ACCESS_REQUEST = {
        "name": "accept_access_request",
        "endpoint": "/access-request/update-access-request",
    }
    REJECT_ACCESS_REQUEST = {
        "name": "reject_access_request",
        "endpoint": "/access-request/update-access-request",
    }

    # User Management
    LIST_USERS = {
        "name": "list_users",
        "endpoint": "/user-management/list-data-users",
    }
    INSPECT_USER = {
        "name": "inspect_user",
        "endpoint": "/user-management/inspect-data-user",
    }
    CREATE_USER = {
        "name": "create_user",
        "endpoint": "/user-management/create-data-user",
    }
    DELETE_USER = {
        "name": "deactivate_user",
        "endpoint": "/user-management/delete-data-user",
    }

    # Data Operation Rule Management
    LIST_DATA_OP_RULES = {
        "name": "list_data_op_rules",
        "endpoint": "/data-op-rule/list-data-op-rule",
    }
    INSPECT_DATA_OP_RULE = {
        "name": "inspect_data_op_rule",
        "endpoint": "/data-op-rule/inspect-data-op-rule",
    }
    CREATE_DATA_OP_RULE = {
        "name": "create_data_op_rule",
        "endpoint": "/data-op-rule/create-data-op-rule",
    }
    UPDATE_DATA_OP_RULE = {
        "name": "update_data_op_rule",
        "endpoint": "/data-op-rule/update-data-op-rule",
    }
    DELETE_DATA_OP_RULE = {
        "name": "delete_data_op_rule",
        "endpoint": "/data-op-rule/delete-data-op-rule",
    }
