"""Render gitlab api urls module."""


def get_repositories_url(gitlab_url: str, project_id: int) -> str:
    return f"{gitlab_url}/api/v4/projects/{project_id}/registry/repositories"


def get_tags_url(gitlab_url: str, project_id: int, repository_id: int) -> str:
    return f"{gitlab_url}/api/v4/projects/{project_id}/registry/repositories/{repository_id}/tags"


def get_single_tag_url(
    gitlab_url: str, project_id: int, repository_id: int, tag_name: str
) -> str:
    return f"{gitlab_url}/api/v4/projects/{project_id}/registry/repositories/{repository_id}/tags/{tag_name}"
