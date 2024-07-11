from governance_ui.logs import logger


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
            "id": request.id,
            "description": "Request to approve " + request.code.service_func_name,
            "request_time": request.request_time,
            "requesting_user_name": request.requesting_user_name,
            "requesting_user_email": request.requesting_user_email,
            "status": request.status.name,
            "code": request.code.show_code,
        }
        for request in project.requests
    ]

    project_info = {
        "project_name": project.name,
        "project_description": project.description,
        "created_by": project.created_by,
        "requests": project_requests,
    }

    logger.info("List access requests", client=client, action_id="list_access_requests")

    return project_info
