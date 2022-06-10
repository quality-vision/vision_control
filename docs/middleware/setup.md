# Setup

Install [Poetry](https://python-poetry.org), install the dependencies and create a new virtual environment:

```shell
$ poetry install
$ poetry shell
```

Add [pre-commit](https://pre-commit.com) hooks[^1]:

```shell
$ pre-commit install
```

Create an `.env` file containing [required environment variables](#environment-variables).

## Configurations

There are three different configurations for the middleware:

* `development` (default)
* `test`
* `production`

!!! tips
    A different config can be specified with `--settings=vision_control.settings.<config>`.

## Environment variables

Environment variables are either read from the current environment or from a file called `.env`, inside the project root directory.

| Name                     | Default | Description                                                    |
|--------------------------|:-------:|----------------------------------------------------------------|
| `ALLOWED_HOSTS`          | `['*']` | Hosts allowed to access the server.                            |
| `DEBUG`                  | `True`  | Debug mode enabled.                                            |
| `GITLAB_ACCESS_TOKEN`    |  ⚠️[^2]  | Personal access token[^3] from GitLab.                         |
| `GITLAB_DEFAULT_PROJECT` |  ⚠️[^2]  | GitLab project id[^4] to use when no other has been selected.  |
| `GITLAB_PROJECT_IDS`     |  `[]`   | GitLab project id:s[^4] to use when fetching data from GitLab. |
| `GITLAB_URL`             |  ⚠️[^2]  | Base URL of GitLab instance to use.                            |
| `GRAFANA_ACCESS_TOKEN`   |  ⚠️[^2]  | Access token[^5] from Grafana.                                 |
| `LANGUAGE_CODE`          | `en-us` |                                                                |
| `SECRET_KEY`             |  ❗️[^6]  | Django secret key. **Must** be changed in production.         |
| `TIME_ZONE`              |  `UTC`  |                                                                |

[^1]: Used for validating commits.
[^2]: Must always be set manually.
[^3]: [GitLab Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokenshtml)
[^4]: [GitLab Projects API](https://docs.gitlab.com/ee/user/profile/personal_access_tokenshtml)
[^5]: [Grafana Access Token](https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token)
[^6]: `django-insecure-(19l&*=hkp8pbfiqh1%s839xzv+5y60=n7de&f*0zx=0!%%#fy`
