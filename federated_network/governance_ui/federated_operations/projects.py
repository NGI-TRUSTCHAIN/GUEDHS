from governance_ui.actions import PySyftActions
from governance_ui.logs import logger
import pandas as pd
from governance_ui.federated_operations.utils import override_input


def get_projects(client):
    projects = client.projects.get_all()
    logger.info(
        "List access requests",
        client=client,
        action=PySyftActions.LIST_ACCESS_REQUESTS.value,
    )

    if len(projects) == 0:
        return []

    data = [
        {
            "index": project_index,
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_by": project.created_by,
            "total_requests": len(project.requests),
            "pending_requests": project.pending_requests,
            "requests": get_all_requests(client, project),
        }
        for project_index, project in enumerate(projects)
    ]

    return data


def get_all_requests_by_project_id(client, project_id):
    project = client.projects.get_by_uid(project_id)
    logger.info(
        "List access requests",
        client=client,
        action=PySyftActions.LIST_ACCESS_REQUESTS.value,
    )

    return get_all_requests(client, project)


def get_all_requests(client, project):
    logger.info("Listing access requests", client=client, action_id="list_access_requests")

    return [get_request(client, request, request_index) for request_index, request in enumerate(project.requests)]


def get_request_by_project_id(client, project_id, request_index):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    return get_request(client, request, request_index)


def get_request(client, request, request_index):
    logger.info(
        "Inspecting access request",
        client=client,
        action=PySyftActions.INSPECT_ACCESS_REQUEST.value,
        user_id=request.requesting_user_email,
        dataset_id=str(request.code.assets[0].id),  # FIX: Assuming only one dataset
        status=request.status.name,
        request_access_id=str(request.id),
    )

    return {
        "index": request_index,
        "id": request.id,
        "description": "Request to approve " + request.code.service_func_name,
        "request_time": request.request_time,
        "requesting_user_name": request.requesting_user_name,
        "requesting_user_email": request.requesting_user_email,
        "status": request.status.name,
        "function_name": request.code.service_func_name,
        "function_code": request.code.raw_code,
        "datasets": [
            {
                "asset_id": asset.id,
                "asset_name": asset.name,
                # "asset_description": asset.description,
                "uploader_name": asset.uploader.name,
                "uploader_email": asset.uploader.email,
                "created_at": asset.created_at,
                "mock_data": pd.DataFrame(asset.mock[:8], dtype=str),
                "private_data": pd.DataFrame(asset.data[:8], dtype=str),
            }
            for asset in request.code.assets
        ],
    }


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


def approve_request(client, project_id, request_index, real_result):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    logger.info(
        "Accept access request",
        client=client,
        action=PySyftActions.ACCEPT_ACCESS_REQUEST.value,
        user_id=request.requesting_user_email,
        dataset_id=str(request.code.assets[0].id),
        status=request.status.name,
        request_access_id=str(request.id),
    )

    # request.accept_by_depositing_result(real_result, force=True)
    override_input(request.accept_by_depositing_result, real_result, force=True)


def reject_request(client, project_id, request_index, reason):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    logger.info(
        "Reject access request",
        client=client,
        action=PySyftActions.REJECT_ACCESS_REQUEST.value,
        user_id=request.requesting_user_email,
        dataset_id=str(request.code.assets[0].id),
        status=request.status.name,
        request_access_id=request.id,
    )

    # request.deny(reason=reason)
    override_input(request.deny, reason=reason)
