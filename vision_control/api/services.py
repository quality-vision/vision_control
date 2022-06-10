from django.conf import settings

import sys
import logging

log = logging.getLogger(__name__)

import hooks
import gitlab as gitlab_api

from .adapters.gitlab import GitLabMetricsAdapter, GitLabVariablesAdapter
from .adapters.vision_control import VisionControlMetricsAdapter
from .grafana_json_datasource import GrafanaJSONDatasource

gitlab = gitlab_api.Gitlab(
    url=settings.GITLAB_URL, private_token=settings.GITLAB_ACCESS_TOKEN
)

if not settings.GITLAB_URL:
    log.error(
        "GITLAB_URL missing from environment. Make sure it is configured properly."
    )
    sys.exit(1)

if not settings.GITLAB_ACCESS_TOKEN:
    log.error(
        "GITLAB_ACCESS_TOKEN missing from environment. Make sure it is configured properly."
    )
    sys.exit(1)

try:
    gitlab.auth()
except gitlab_api.exceptions.GitlabAuthenticationError as e:
    log.error(
        "Authentication to GitLab failed. Make sure GITLAB_URL and GITLAB_ACCESS_TOKEN are configured properly."
    )
    sys.exit(1)

log.info(f"Authenticated to {settings.GITLAB_URL}.")

try:
    project = gitlab.projects.get(settings.GITLAB_DEFAULT_PROJECT)
except gitlab_api.GitlabGetError:
    log.error(
        f"Project #{settings.GITLAB_DEFAULT_PROJECT} does not exist. Make sure that GITLAB_DEFAULT_PROJECT is set to an existing Gitlab project."
    )
    sys.exit(1)

log.info(
    f"Using '{project.name}' (#{settings.GITLAB_DEFAULT_PROJECT}) as default project for queries."
)

hooks.configure(gitlab)

vision_control_metrics_adapter = VisionControlMetricsAdapter()
gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
gitlab_variables_adapter = GitLabVariablesAdapter(gitlab)
datasource = GrafanaJSONDatasource()

datasource.add_metrics(
    "gitlab",
    {
        "commits": gitlab_metrics_adapter.commits,
        "users": gitlab_metrics_adapter.users,
        "pipelines": gitlab_metrics_adapter.pipelines,
        "issues": gitlab_metrics_adapter.issues,
        "merge_requests": gitlab_metrics_adapter.merge_requests,
        "milestones": gitlab_metrics_adapter.milestones,
    },
)

datasource.add_metrics(
    "vision_control", {"version": vision_control_metrics_adapter.version}
)

datasource.add_variables(
    "gitlab",
    {
        "projects": gitlab_variables_adapter.projects,
        "branches": gitlab_variables_adapter.branches,
        "labels": gitlab_variables_adapter.labels,
    },
)
