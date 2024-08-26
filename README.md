# gitlab_registry_cleaner

A project can remove tags from the gitlab registry by configuration file.

Supported time:
1. **days**
2. **hours**
3. **minutes**

Environments:
1. GITLAB_TOKEN - personal gitlab token. Override from CLI **-t** or **--token**.
2. GITLAB_URL - general gitlab domain, https://gitlab.com for example. Override from CLI **--url**.
3. REPOSITORY_CONFIG_PATH - path to json config file. Override from CLI **-c** or **--config**.
4. SSL_PATH - path to SSL certificate. Override from CLI **--ssl_path**.
5. TIMEOUT - timeout to all HTTP requests. Override from CLI **--timeout**.

Also, you can set **--dry-run** flag from CLI. In this mode found tags not be deleted.

# Install
```bash
pip install gitlab_registry_async_cleaner
```

# Usage
```bash
gitlab_async_cleaner
```
You can create an .env file in your startup directory or set environment 
variables any way you like. The CLI takes precedence and arguments passed
through the CLI will change the environment variables.

JSON config example
```json
{
  "gitlab_project_1":
  {
    "id": 1,
    "delete_older_than": {
      "days": 2
    }
  },
  "gitlab_project_2":
  {
    "id": 2,
    "delete_older_than": {
      "hours": 5
    }
  },
  "gitlab_project_3":
  {
    "id": 3,
    "delete_older_than": {
      "minutes": 60
    }
  }
}
```