from governance_ui.modules.datasets import datasets_ui, register_dataset_ui
from governance_ui.modules.projects import projects_ui
from governance_ui.icons import database_icon, database_add_icon, file_icon


sections = {
    "datasets": {
        "button_id": "show_datasets_button",
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
        "icon": file_icon,
        "button_text": "Projects",
        "ui": projects_ui("projects"),
    },
}
