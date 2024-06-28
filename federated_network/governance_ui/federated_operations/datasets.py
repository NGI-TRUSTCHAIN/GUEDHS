import syft as sy
import pandas as pd
from unittest.mock import patch

def get_datasets_table(datasets):
    if datasets is None:
        return None

    data = [
        {
            "id": f"{str(dataset.id)[:8]}...",
            "name": dataset.name,
            "updated at": dataset.updated_at,
            "created at": dataset.created_at
        }
        for dataset in datasets
    ]

    df = pd.DataFrame(data)
    df = df.sort_values(by="created at", ascending=False)

    styled_df = df.style.hide(axis="index").set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#e5e7eb"),
                    ("padding", "10px 15px"),
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("background-color", "#f3f4f6"),
                    ("padding", "10px 15px")
                ]
            }
        ]
    ).set_table_attributes(
        'style="border-radius: 10px; overflow: hidden;"'
    )

    return styled_df


def override_input(func, *args, **kwargs):
    with patch("builtins.input", return_value="y") as mock_input:
        return func(*args, **kwargs)


def register_dataset(client, dataset_name, dataset_description, asset_name, asset_description, data_path):
    main_data_subject = sy.DataSubject(
        name="Clinical",
        aliases=["clinical"],
        description="",
    )

    data_subject = sy.DataSubject(
        name="Clinical DataSubject",
        aliases=["clinical:ds"],
        description="",
    )

    main_data_subject.add_member(data_subject)
    client.data_subject_registry.add_data_subject(main_data_subject)

    dataset = sy.Dataset(
        name = dataset_name,
        description = dataset_description,
    )

    # Verify if dataset is an URL or a Path
    if isinstance(data_path, str) and data_path.startswith("http"):
        print("Downloading data from URL...")
        data = pd.read_csv(sy.autocache(data_path))
    else:
        print("Reading data from file...")
        data = pd.read_csv(data_path[0]["datapath"])

    mock = data.sample(frac=0.1)

    asset = sy.Asset(
        name = asset_name,
        description = asset_description,
    )
    asset.set_obj(data)
    asset.set_mock(mock, mock_is_real=True)
    asset.set_shape(data.shape)
    asset.add_data_subject(data_subject)

    dataset.add_asset(asset)
    # client.upload_dataset(dataset)
    override_input(client.upload_dataset, dataset)

    print(f"Dataset \"{dataset_name}\" registered successfully!")

