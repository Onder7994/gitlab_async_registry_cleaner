"""Hander module."""

import asyncio
from datetime import timedelta
from gitlab_registry_async_cleaner.gitlab.image_registry_process import (
    get_repositories,
    process_tags,
)
from gitlab_registry_async_cleaner.cli.cli import GitlabConfig
from gitlab_registry_async_cleaner.logger.logger import Logging

logger = Logging(__name__)


async def convert_to_timedelta(repo_delete_older_than: dict) -> timedelta:
    """Convert dict to timedelta."""
    if "days" in repo_delete_older_than:
        return timedelta(days=repo_delete_older_than["days"])
    if "hours" in repo_delete_older_than:
        return timedelta(hours=repo_delete_older_than["hours"])
    if "minutes" in repo_delete_older_than:
        return timedelta(minutes=repo_delete_older_than["minutes"])
    else:
        raise ValueError("Unsupported time unit %s", repo_delete_older_than)


async def create_async_tasks(
    json_config: dict,
    config: GitlabConfig,
) -> None:
    """Create async tasks to clean project repos."""
    headers = {"PRIVATE-TOKEN": config.gitlab_token}
    tasks = []
    for name, value in json_config.items():
        repo_name = name
        repo_id = value["id"]
        repo_delete_older_than = value["delete_older_than"]
        repo_delete_delta = await convert_to_timedelta(repo_delete_older_than)
        logger.info("Start processing project: %s", repo_name)
        tasks.append(
            process_project(
                repo_name=repo_name,
                repo_id=repo_id,
                repo_delete_delta=repo_delete_delta,
                headers=headers,
                config=config,
            )
        )
    await asyncio.gather(*tasks)


async def process_project(
    repo_name: str,
    repo_id: int,
    repo_delete_delta: timedelta,
    headers: dict,
    config: GitlabConfig,
) -> None:
    """Processing project."""
    registry_repository = await get_repositories(
        registry_project_id=repo_id,
        headers=headers,
        config=config,
    )
    if registry_repository is not None:
        for repository_id, _ in registry_repository.items():
            await process_tags(
                registry_project_id=repo_id,
                repository_id=repository_id,
                headers=headers,
                config=config,
                delete_older_than=repo_delete_delta,
            )
    else:
        logger.error("Can't get data from repository %s", repo_name)
