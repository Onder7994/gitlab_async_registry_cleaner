"""Gitlab module."""

from datetime import timedelta, datetime, timezone
from typing import Dict, Any

from gitlab_registry_async_cleaner.api_requests.requests import (
    send_api_get_request,
    send_api_delete_request,
)
from gitlab_registry_async_cleaner.cli.cli import GitlabConfig
from gitlab_registry_async_cleaner.gitlab.api_urls import (
    get_repositories_url,
    get_tags_url,
    get_single_tag_url,
)
from gitlab_registry_async_cleaner.logger.logger import Logging

logger = Logging(__name__)


async def get_repositories(
    registry_project_id: int,
    headers: dict,
    config: GitlabConfig,
) -> Dict[Any, dict[str, Any]] | None:
    """Get all repositories from gitlab project."""
    repositories_dict = {}
    url = get_repositories_url(
        gitlab_url=config.gitlab_url,
        project_id=registry_project_id,
    )
    data = await send_api_get_request(
        url=url,
        timeout=config.timeout,
        headers=headers,
        verify=config.ssl_path,
    )
    if data is not None:
        if data.status_code == 200:
            total_page_number = int(data.headers["X-Total-Pages"])
            current_page_number = int(data.headers["X-Page"])
            while current_page_number <= total_page_number:
                response = await send_api_get_request(
                    url=url,
                    timeout=config.timeout,
                    headers=headers,
                    verify=config.ssl_path,
                    params={"page": current_page_number},
                )
                repositories = response.json()
                for _, item in enumerate(repositories):
                    repositories_dict[item["id"]] = {
                        "name": item["name"],
                        "path": item["path"],
                    }
                current_page_number += 1
            return repositories_dict
        else:
            logger.error(
                "Failed request to %s with status: %s and message: %s",
                url,
                data.status_code,
                data.text,
            )
            return None
    else:
        logger.error("Failed read data from %s", url)


async def process_tags(
    registry_project_id: int,
    repository_id: int,
    headers: dict,
    config: GitlabConfig,
    delete_older_than: timedelta,
) -> None:
    """Processing tags in repositories."""
    url = get_tags_url(
        gitlab_url=config.gitlab_url,
        project_id=registry_project_id,
        repository_id=repository_id,
    )
    data = await send_api_get_request(
        url=url,
        timeout=config.timeout,
        headers=headers,
        verify=config.ssl_path,
    )
    if data is not None:
        if data.status_code == 200:
            total_page_number = int(data.headers["X-Total-Pages"])
            current_page_number = int(data.headers["X-Page"])
            while current_page_number <= total_page_number:
                response = await send_api_get_request(
                    url=url,
                    timeout=config.timeout,
                    headers=headers,
                    verify=config.ssl_path,
                    params={"page": current_page_number},
                )
                repository_tags = response.json()
                for _, item in enumerate(repository_tags):
                    tag_name = item["name"]
                    await process_single_tag_and_delete(
                        registry_project_id=registry_project_id,
                        repository_id=repository_id,
                        tag_name=tag_name,
                        headers=headers,
                        config=config,
                        delete_older_than=delete_older_than,
                    )
                current_page_number += 1
        else:
            logger.error(
                "Failed request to %s with status: %s and message: %s",
                url,
                data.status_code,
                data.text,
            )
    else:
        logger.error("Failed read data from %s", url)


async def process_single_tag_and_delete(
    registry_project_id: int,
    repository_id: int,
    tag_name: str,
    headers: dict,
    config: GitlabConfig,
    delete_older_than: timedelta,
) -> None:
    """Process single tag and delete if need."""
    url = get_single_tag_url(
        gitlab_url=config.gitlab_url,
        project_id=registry_project_id,
        repository_id=repository_id,
        tag_name=tag_name,
    )
    tag_info = await send_api_get_request(
        url=url,
        timeout=config.timeout,
        headers=headers,
        verify=config.ssl_path,
    )
    if tag_info is not None:
        if tag_info.status_code == 200:
            tag_info = tag_info.json()
            is_tag_mark_to_delete = await is_tag_expired(
                tag_created=tag_info["created_at"], delete_older_than=delete_older_than
            )
            logger.info(
                "Processing repository tag.",
                extra={
                    "operation": "processing",
                    "tag_location": tag_info["location"].rsplit(":", 1)[0],
                    "tag_name": tag_info["name"],
                },
            )
            if is_tag_mark_to_delete:
                await delete_tag(
                    registry_project_id=registry_project_id,
                    repository_id=repository_id,
                    tag_name=tag_name,
                    headers=headers,
                    config=config,
                    tag_path=tag_info["location"].rsplit(":", 1)[0],
                )
        else:
            logger.error(
                "Failed request to %s. Status: %s. Message: %s",
                url,
                tag_info.status_code,
                tag_info.text,
            )
    else:
        logger.error("Failed read data from %s", url)


async def delete_tag(
    registry_project_id: int,
    repository_id: int,
    tag_name: str,
    tag_path: str,
    headers: dict,
    config: GitlabConfig,
) -> None:
    """Delete tag."""
    url = get_single_tag_url(
        gitlab_url=config.gitlab_url,
        project_id=registry_project_id,
        repository_id=repository_id,
        tag_name=tag_name,
    )
    if config.dry_run:
        logger.warning(
            "Dry run mode enabled. Tag not deleted",
            extra={
                "operation": "dry_run",
                "tag_name": tag_name,
                "tag_location": tag_path,
            },
        )
    else:
        logger.info(
            "Delete tag.",
            extra={
                "operation": "deleted",
                "tag_name": tag_name,
                "tag_location": tag_path,
            },
        )
        await send_api_delete_request(
            url=url,
            timeout=config.timeout,
            headers=headers,
            verify=config.ssl_path,
        )


async def is_tag_expired(tag_created: str, delete_older_than: timedelta) -> bool | None:
    """Check if tag is expired."""
    try:
        tag_date = datetime.fromisoformat(tag_created)
        now = datetime.now(timezone.utc)
        return tag_date < now - delete_older_than
    except TypeError:
        logger.warning("Can't read created_at filed: Value: %s", tag_created)
