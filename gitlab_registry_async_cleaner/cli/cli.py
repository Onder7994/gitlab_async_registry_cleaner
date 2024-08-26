"""CLI module."""

import argparse
import os
from dataclasses import dataclass


@dataclass
class GitlabConfig:
    """Gitlab parameters."""

    gitlab_token: str
    gitlab_url: str
    config: str
    dry_run: bool
    ssl_path: str
    timeout: int


def create_parser() -> tuple[argparse.ArgumentParser, GitlabConfig]:
    """CLI parser method."""
    parser = argparse.ArgumentParser(description="Gitlab registry cleaner")
    parser.add_argument(
        "-t",
        "--token",
        dest="gitlab_token",
        required=False,
        default=os.environ.get("GITLAB_TOKEN"),
        help="Gitlab token",
    )
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        dest="gitlab_url",
        default=os.environ.get("GITLAB_URL"),
        help="GITLAB URL",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        required=False,
        default=os.environ.get("REPOSITORY_CONFIG_PATH"),
        help="Path to gitlab repository config",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        dest="dry_run",
        required=False,
        action="store_true",
        help="Run in dry run mode. Without delete tags.",
    )
    parser.add_argument(
        "--ssl-path",
        dest="ssl_path",
        required=False,
        default=os.environ.get("SSL_PATH", False),
        help="Path to SSL gitlab certificate.",
    )
    parser.add_argument(
        "--timeout",
        dest="timeout",
        required=False,
        default=os.environ.get("TIMEOUT", 20),
        help="HTTP request timeout.",
    )
    args = parser.parse_args()
    config = GitlabConfig(
        gitlab_token=args.gitlab_token,
        gitlab_url=args.gitlab_url,
        config=args.config,
        dry_run=args.dry_run,
        ssl_path=args.ssl_path,
        timeout=args.timeout,
    )
    return parser, config
