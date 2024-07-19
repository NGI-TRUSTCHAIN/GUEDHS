from governance_ui.logs import logger
import pandas as pd
from unittest.mock import patch


def get_projects(client):
    projects = client.projects.get_all()

    if len(projects) == 0:
        return []

    data = [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_by": project.created_by,
            "total_requests": len(project.requests),
            "pending_requests": project.pending_requests,
        }
        for project in projects
    ]

    return data


def get_project_info(client, project_id):
    project = client.projects.get_by_uid(project_id)

    if project is None:
        return {}

    project_requests = [
        {
            "index": index,
            "id": request.id,
            "description": "Request to approve " + request.code.service_func_name,
            "request_time": request.request_time,
            "requesting_user_name": request.requesting_user_name,
            "requesting_user_email": request.requesting_user_email,
            "status": request.status.name,
        }
        for index, request in enumerate(project.requests)
    ]

    project_info = {
        "project_name": project.name,
        "project_description": project.description,
        "created_by": project.created_by,
        "requests": project_requests,
    }

    logger.info("List access requests", client=client, action_id="list_access_requests")

    return project_info


def get_request_info(client, project_id, request_index):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]
    dataset_info = {}

    if len(request.code.assets) > 0:
        asset = request.code.assets[0]

        dataset_info = {
            "asset_id": asset.id,
            "asset_name": asset.name,
            # "asset_description": asset.description,
            "uploader_name": asset.uploader.name,
            "uploader_email": asset.uploader.email,
            "created_at": asset.created_at,
            "mock_data": pd.DataFrame(asset.mock[:8], dtype=str),
            "private_data": pd.DataFrame(asset.data[:8], dtype=str),
        }

    request_info = {
        "id": request.id,
        "description": "Request to approve " + request.code.service_func_name,
        "requesting_user_name": request.requesting_user_name,
        "requesting_user_email": request.requesting_user_email,
        "request_time": request.request_time,
        "status": request.status.name,
        "function_name": request.code.service_func_name,
        "function_code": request.code.raw_code,
        "dataset_info": dataset_info,
    }

    return request_info


def execute_code(client, project_id, request_index):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]
    func = request.code

    if len(func.assets) == 0:
        return None, None

    asset = func.assets[0]

    input_keys = func.input_kwargs
    users_function = func.unsafe_function

    kwargs1 = {input_keys[0]: asset.mock}

    mock_result = users_function(**kwargs1)

    kwargs2 = {input_keys[0]: asset.data}

    real_result = users_function(**kwargs2)

    return mock_result, real_result


def override_input(func, *args, **kwargs):
    with patch("builtins.input", return_value="y"):
        return func(*args, **kwargs)


def approve_request(client, project_id, request_index, real_result):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    # request.accept_by_depositing_result(real_result, force=True)
    override_input(request.accept_by_depositing_result, real_result, force=True)


def reject_request(client, project_id, request_index, reason):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    # request.deny(reason=reason)
    override_input(request.deny, reason=reason)
