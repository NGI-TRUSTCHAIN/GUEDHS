import syft as sy
import pandas as pd
from governance_ui.federated_operations.utils import override_input
from governance_ui.logs import logger
from datetime import datetime


def get_datasets(client):
    datasets = client.datasets.get_all()

    if len(datasets) == 0:
        return []

    data = [
        {
            "id": dataset.id,
            "name": dataset.name,
            "created_at": dataset.created_at,
            "updated_at": dataset.updated_at,
        }
        for dataset in datasets
    ]

    logger.info("Listing datasets", client=client, action_id="list_datasets")

    return data


def register_dataset(
    client, dataset_name, dataset_description, asset_name, asset_description, data_path, mock_path, mock_is_real
):
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
        name=dataset_name,
        description=dataset_description,
        id=sy.UID(),
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    # Verify if dataset is an URL or a Path
    if isinstance(data_path, str) and data_path.startswith("http"):
        print("Downloading data from URL...")
        data = pd.read_csv(sy.autocache(data_path), low_memory=False)
    else:
        print("Reading data from file...")
        data = pd.read_csv(data_path[0]["datapath"], low_memory=False)

    asset = sy.Asset(
        name=asset_name,
        description=asset_description,
    )
    asset.set_obj(data)
    asset.set_shape(data.shape)
    asset.add_data_subject(data_subject)

    # Verify if mock is an URL or a Path or None
    if mock_path is not None:
        if isinstance(mock_path, str) and mock_path.startswith("http"):
            print("Downloading mock from URL...")
            mock = pd.read_csv(sy.autocache(mock_path), low_memory=False)
        else:
            print("Reading mock from file...")
            mock = pd.read_csv(mock_path[0]["datapath"], low_memory=False)
        asset.set_mock(mock, mock_is_real=mock_is_real)
    else:
        print("Creating mock...")
        mock = data.sample(frac=0.1)
        asset.set_mock(mock, mock_is_real=True)

    dataset.add_asset(asset)
    # client.upload_dataset(dataset)
    override_input(client.upload_dataset, dataset)

    logger.info(
        "Dataset registered",
        client=client,
        action_id="register_dataset",
        dataset_id=str(dataset.id),
    )


def get_dataset_info(client, dataset_id):
    dataset = client.datasets.get_by_id(sy.UID(dataset_id))

    mock = dataset.asset_list[0].mock[:8]
    mock_df = pd.DataFrame(mock, dtype=str)

    dataset_info = {
        "dataset_name": str(dataset.name),
        "dataset_description": dataset.description.text,
        "data_subject": dataset.asset_list[0].data_subjects[0].name,
        "asset_name": dataset.asset_list[0].name,
        # "asset_description": dataset.asset_list[0].description.text,
        "data_shape": dataset.asset_list[0].shape,
        "mock": dataset.asset_list[0].mock,
        "mock_shape": dataset.asset_list[0].mock.shape,
        "mock_is_real": dataset.asset_list[0].mock_is_real,
        "mock_df": mock_df,
    }

    logger.info(
        "Inspecting dataset",
        client=client,
        action_id="inspect_dataset",
        dataset_id=dataset_id,
    )

    return dataset_info
