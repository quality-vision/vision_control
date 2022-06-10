from django.conf import settings

from datetime import datetime

import emoji
import gitlab.exceptions

from ..utils import unix_timestamp
from ..grafana_json_datasource import Table, TimeSeries, TableColumn, TableColumnType
from ..grafana_json_datasource.exceptions import ProjectDoesNotExistError


class GitLabMetricsAdapter:
    """The purpose of this class is to interpret Grafana metric queries and return the requested information from Gitlab."""

    def __init__(self, gitlab):
        self.gitlab = gitlab

    def commits(self, payload, interval):
        project_id = payload.get("project", settings.GITLAB_DEFAULT_PROJECT)
        try:
            project = self.gitlab.projects.get(project_id)
        except gitlab.exceptions.GitlabGetError:
            raise ProjectDoesNotExistError(project_id)
        branch = payload.get("branch", None)
        commits = project.commits.list(
            ref_name=branch, all=True, since=interval.start, until=interval.end
        )
        timeseries = payload.get("timeseries", False)

        if timeseries:
            return self._commits_timeseries(commits)
        else:
            return self._commits_table(commits)

    def _commits_table(self, commits) -> Table:
        return Table(
            [
                TableColumn("Time", TableColumnType.TIME),
                TableColumn("Author", TableColumnType.STRING),
                TableColumn("Message", TableColumnType.STRING),
            ],
            [
                [
                    unix_timestamp(
                        datetime.strptime(
                            commit.committed_date, "%Y-%m-%dT%H:%M:%S.%f%z"
                        )
                    ),
                    commit.author_name,
                    commit.message,
                ]
                for commit in commits
            ],
        )

    def _commits_timeseries(self, commits) -> TimeSeries:
        return TimeSeries(
            [
                [
                    1,
                    unix_timestamp(
                        datetime.strptime(
                            commit.committed_date, "%Y-%m-%dT%H:%M:%S.%f%z"
                        )
                    ),
                ]
                for commit in commits
            ]
        )

    def users(self, *_):
        # FIXME: Replace with a full query for all users.
        # users = self.gitlab.users.list()
        # We used LiU:s Gitlab while developing this and the query took to long to be able to list all users.
        users = [
            self.gitlab.users.get(1806),
            self.gitlab.users.get(1872),
            self.gitlab.users.get(1826),
            self.gitlab.users.get(1902),
            self.gitlab.users.get(2033),
            self.gitlab.users.get(2011),
            self.gitlab.users.get(1876),
        ]

        result = Table(
            [
                TableColumn("id", TableColumnType.NUMERIC),
                TableColumn("name", TableColumnType.STRING),
                TableColumn("username", TableColumnType.STRING),
                TableColumn("avatar_url", TableColumnType.STRING),
                TableColumn("public_email", TableColumnType.STRING),
                TableColumn("active", TableColumnType.BOOLEAN),
                TableColumn("busy", TableColumnType.BOOLEAN),
                TableColumn("status_emoji", TableColumnType.STRING),
                TableColumn("status_message", TableColumnType.STRING),
            ],
            [],
        )

        for user in users:
            status = user.status.get()

            if status.emoji:
                status_emoji = (emoji.emojize(f":{status.emoji}:", language="alias"),)
            else:
                status_emoji = ""

            result.rows.append(
                [
                    user.id,
                    user.name,
                    user.username,
                    user.avatar_url,
                    user.public_email,
                    user.state == "active",
                    status.availability == "busy",
                    status_emoji,
                    status.message,
                ]
            )

        return result

    def pipelines(self, payload, interval):
        project_id = payload.get("project", settings.GITLAB_DEFAULT_PROJECT)

        try:
            project = self.gitlab.projects.get(project_id)
        except gitlab.exceptions.GitlabGetError:
            raise ProjectDoesNotExistError(project_id)
        branch = payload.get("branch", None)
        pipelines = project.pipelines.list(
            all=True,
            updated_after=interval.start,
            updated_before=interval.end,
            ref=branch,
        )

        return Table(
            [
                TableColumn("Time", TableColumnType.TIME),
                TableColumn("Ref name", TableColumnType.STRING),
                TableColumn("Status", TableColumnType.STRING),
                TableColumn("ID", TableColumnType.NUMERIC),
                TableColumn("Triggered by", TableColumnType.STRING),
                TableColumn("URL", TableColumnType.STRING),
            ],
            [
                [
                    unix_timestamp(
                        datetime.strptime(pipeline.created_at, "%Y-%m-%dT%H:%M:%S.%f%z")
                    ),
                    pipeline.ref,
                    pipeline.status,
                    pipeline.id,
                    project.commits.get(pipeline.sha).author_name,
                    pipeline.web_url,
                ]
                for pipeline in pipelines
            ],
        )

    def issues(self, payload, interval):
        project_id = payload.get("project", settings.GITLAB_DEFAULT_PROJECT)
        project = self.gitlab.projects.get(project_id)
        state = payload.get("state")
        labels = payload.get("labels", [])
        all = payload.get("all", False)

        issues = project.issues.list(
            all=True,
            labels=labels,
            state=state,
            updated_after=None if all else interval.start,
            updated_before=None if all else interval.end,
        )

        return Table(
            [
                TableColumn("ID", TableColumnType.NUMERIC),
                TableColumn("title", TableColumnType.STRING),
                TableColumn("labels", TableColumnType.STRING),
                TableColumn("state", TableColumnType.STRING),
                TableColumn("updated_at", TableColumnType.TIME),
            ],
            [
                [issue.id, issue.title, issue.labels, issue.state, issue.updated_at]
                for issue in issues
            ],
        )

    def merge_requests(self, payload, interval):
        project_id = payload.get("project", settings.GITLAB_DEFAULT_PROJECT)
        merge_request_status = payload.get("status", "all")
        branch = payload.get("branch", "main")
        project = self.gitlab.projects.get(project_id)
        merge_requests = project.mergerequests.list(
            state=merge_request_status,
            ref=branch,
            updated_after=interval.start,
            updated_before=interval.end,
            all=True,
        )

        return Table(
            [
                TableColumn("Status", TableColumnType.STRING),
                TableColumn("Source branch", TableColumnType.STRING),
                TableColumn("Target branch", TableColumnType.STRING),
                TableColumn("Author", TableColumnType.STRING),
                TableColumn("Created at", TableColumnType.TIME),
            ],
            [
                [
                    merge_request.state,
                    merge_request.source_branch,
                    merge_request.target_branch,
                    merge_request.author["name"],
                    merge_request.created_at,
                ]
                for merge_request in merge_requests
            ],
        )

    def milestones(self, payload, _=None):
        """Extracts the milestones from a given project. Can be filtered by state, but otherwise gets all milestones for a project."""
        project_id = payload.get("project", settings.GITLAB_DEFAULT_PROJECT)
        project = self.gitlab.projects.get(project_id)

        milestone_state = payload.get("state", None)
        if milestone_state == "All":
            milestone_state = None

        milestone_list = project.milestones.list(
            state=milestone_state,
        )

        return Table(
            [
                TableColumn("Title", TableColumnType.STRING),
                TableColumn("ID", TableColumnType.NUMERIC),
                TableColumn("Status", TableColumnType.STRING),
                TableColumn("Description", TableColumnType.STRING),
                TableColumn("Start date", TableColumnType.TIME),
                TableColumn("Due date", TableColumnType.TIME),
                TableColumn("Expired", TableColumnType.BOOLEAN),
            ],
            [
                [
                    milestone.title,
                    milestone.iid,
                    milestone.state,
                    milestone.description,
                    milestone.start_date,
                    milestone.due_date,
                    milestone.expired,
                ]
                for milestone in milestone_list
            ],
        )


class GitLabVariablesAdapter:
    def __init__(self, gitlab):
        self.gitlab = gitlab

    def projects(self, _=None):
        projects = [
            self.gitlab.projects.get(project_id)
            for project_id in settings.GITLAB_PROJECT_IDS
        ]

        return {project.name: project.id for project in projects}

    def labels(self, data):
        project_id = data.get("project", settings.GITLAB_DEFAULT_PROJECT)

        try:
            project = self.gitlab.projects.get(project_id)
        except gitlab.exceptions.GitlabGetError:
            raise ProjectDoesNotExistError(project_id)

        labels = project.labels.list()
        return {label.name: label.name for label in labels}

    def branches(self, data):
        project_id = data.get("project", settings.GITLAB_DEFAULT_PROJECT)

        try:
            project = self.gitlab.projects.get(project_id)
        except gitlab.exceptions.GitlabGetError:
            raise ProjectDoesNotExistError(project_id)

        branches = project.branches.list()
        return {branch.name: branch.name for branch in branches}
