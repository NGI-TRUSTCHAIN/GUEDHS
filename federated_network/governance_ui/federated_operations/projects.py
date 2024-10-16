from governance_ui.actions import PySyftActions
from governance_ui.logs import logger
import pandas as pd
from governance_ui.federated_operations.utils import override_input


def get_projects(client):
    logger.info(
        "Listing access requests",
        client=client,
        action=PySyftActions.LIST_ACCESS_REQUESTS.value,
    )
    projects = client.projects.get_all()

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
        "Listing access requests",
        client=client,
        action=PySyftActions.LIST_ACCESS_REQUESTS.value,
    )

    return get_all_requests(client, project)


def get_all_requests(client, project):
    return [get_request(client, request, request_index) for request_index, request in enumerate(project.requests)]


def get_request_by_project_id(client, project_id, request_index):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    return get_request(client, request, request_index)


def get_request(client, request, request_index):
    asset_ids = []
    datasets = {}
    for asset in request.code.assets:
        asset_id = str(asset.id)
        asset_ids.append(asset_id)
        datasets[asset_id] = {
            "id": asset_id,
            "name": asset.name,
            "uploader_name": asset.uploader.name,
            "uploader_email": asset.uploader.email,
            "created_at": asset.created_at,
            "mock_data": pd.DataFrame(asset.mock[:8], dtype=str),
            "private_data": pd.DataFrame(asset.data[:8], dtype=str),
        }

    logger.info(
        "Inspecting access request",
        client=client,
        action=PySyftActions.INSPECT_ACCESS_REQUEST.value,
        user_id=request.requesting_user_email,
        dataset_id=", ".join(asset_ids),
        status=request.status.name,
        request_access_id=str(request.id),
    )

    return {
        "index": request_index,
        "id": str(request.id),
        "description": "Request to approve " + request.code.service_func_name,
        "request_time": request.request_time,
        "requesting_user_name": request.requesting_user_name,
        "requesting_user_email": request.requesting_user_email,
        "status": request.status.name,
        "function_name": request.code.service_func_name,
        "function_code": request.code.raw_code,
        "datasets": datasets,
    }


def execute_code(client, project_id, request_index):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]
    func = request.code

    if len(func.assets) == 0:
        return None, None

    assets = func.assets
    input_keys = func.input_kwargs
    users_function = func.unsafe_function

    kwargs1 = {input_keys[i]: asset.mock for i, asset in enumerate(assets)}
    mock_result = users_function(**kwargs1)

    kwargs2 = {input_keys[i]: asset.data for i, asset in enumerate(assets)}
    real_result = users_function(**kwargs2)

    return mock_result, real_result


def approve_request(client, project_id, request_index, real_result):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    logger.info(
        "Accepting access request",
        client=client,
        action=PySyftActions.ACCEPT_ACCESS_REQUEST.value,
        # user_id=request.requesting_user_email,
        # dataset_id=str(request.code.assets[0].id),
        status="granted",
        request_access_id=str(request.id),
    )

    # request.accept_by_depositing_result(real_result, force=True)
    override_input(request.accept_by_depositing_result, real_result, force=True)


def approve_multiple_requests(client, input_data):
    for data in input_data:
        project_id = data["project_id"]
        request_index = data["request_index"]

        _, real_result = execute_code(client, project_id, request_index)
        approve_request(client, project_id, request_index, real_result)


def reject_request(client, project_id, request_index, reason):
    project = client.projects.get_by_uid(project_id)
    request = project.requests[request_index]

    logger.info(
        "Rejecting access request",
        client=client,
        action=PySyftActions.REJECT_ACCESS_REQUEST.value,
        # user_id=request.requesting_user_email,
        # dataset_id=str(request.code.assets[0].id),
        status="rejected",
        request_access_id=request.id,
    )

    # request.deny(reason=reason)
    override_input(request.deny, reason=reason)


def reject_multiple_requests(client, input_data):
    for data in input_data:
        project_id = data["project_id"]
        request_index = data["request_index"]
        reason = data["reason"]

        reject_request(client, project_id, request_index, reason)
