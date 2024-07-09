from governance_ui.modules.datasets import datasets_ui, register_dataset_ui


sections = {
    "datasets": {"button_id": "show_datasets_button", "button_text": "Datasets", "ui": datasets_ui("datasets")},
    "register_dataset": {
        "button_id": "register_dataset_button",
        "button_text": "Register Dataset",
        "ui": register_dataset_ui("datasets"),
    },
}
