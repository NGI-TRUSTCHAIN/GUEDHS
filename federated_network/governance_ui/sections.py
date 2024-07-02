from governance_ui.view import datasets_ui, register_dataset_ui

sections = {
    "datasets": {"button_id": "show_datasets_button", "button_text": "Datasets", "ui": datasets_ui},
    "register_dataset": {
        "button_id": "register_dataset_button",
        "button_text": "Register Dataset",
        "ui": register_dataset_ui,
    },
}
