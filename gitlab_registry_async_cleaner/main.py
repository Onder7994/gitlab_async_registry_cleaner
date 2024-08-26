"""Main module."""

import asyncio
import os
import sys
from dotenv import load_dotenv
from gitlab_registry_async_cleaner.cli.cli import create_parser
from gitlab_registry_async_cleaner.config_reader.config_reader import read_json_config
from gitlab_registry_async_cleaner.tag_handler import create_async_tasks

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
parser, config = create_parser()


async def async_main():
    """Run async function."""
    json_config = read_json_config(config.config)
    if json_config is None:
        parser.print_help()
        sys.exit(1)
    await create_async_tasks(json_config=json_config, config=config)


def main():
    """Entry point."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
