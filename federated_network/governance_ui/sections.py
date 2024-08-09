from governance_ui.modules.datasets import datasets_ui, register_dataset_ui
from governance_ui.modules.projects import projects_ui
from governance_ui.modules.users import list_users_ui, create_user_ui
from governance_ui.modules.audit_logs import audit_logs_ui
from governance_ui.modules.access_rules import access_rules_ui
from governance_ui.icons import (
    database_icon,
    database_add_icon,
    files_icon,
    user_icon,
    add_user_icon,
    history_icon,
    access_rules_icon,
)


sections = {
    "datasets": {
        "button_id": "list_datasets_button",
        "icon": database_icon,
        "button_text": "Datasets",
        "ui": datasets_ui("datasets"),
    },
    "register_dataset": {
        "button_id": "register_dataset_button",
        "icon": database_add_icon,
        "button_text": "Register Dataset",
        "ui": register_dataset_ui("datasets"),
    },
    "projects": {
        "button_id": "projects_button",
        "icon": files_icon,
        "button_text": "Projects",
        "ui": projects_ui("projects"),
    },
    "access_rules": {
        "button_id": "access_rules_button",
        "icon": access_rules_icon,
        "button_text": "Access Rules",
        "ui": access_rules_ui("access_rules"),
    },
    "users": {
        "button_id": "list_users_button",
        "icon": user_icon,
        "button_text": "Users",
        "ui": list_users_ui("users"),
    },
    "add_user": {
        "button_id": "create_user_button",
        "icon": add_user_icon,
        "button_text": "Create User",
        "ui": create_user_ui("users"),
    },
    "audit_logs": {
        "button_id": "audit_logs_button",
        "icon": history_icon,
        "button_text": "Audit Logs",
        "ui": audit_logs_ui("audit_logs"),
    },
}
