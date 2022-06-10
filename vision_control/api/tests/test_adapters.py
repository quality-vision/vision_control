from django.test import TestCase

from datetime import datetime, timedelta
from collections import namedtuple

import pytest
import gitlab.exceptions

from ..utils import unix_timestamp
from ..adapters.gitlab import GitLabMetricsAdapter, GitLabVariablesAdapter
from ..adapters.vision_control import VisionControlMetricsAdapter
from ..grafana_json_datasource import Table, TimeSeries, TableColumn, TableColumnType
from ..grafana_json_datasource.exceptions import *

# Variables used to mock a GitLab instance.

Project = namedtuple("projects", "get")
Commit = namedtuple("commit", "authored_date committed_date author_name message")
User = namedtuple("user", "id name username avatar_url public_email state status")
Pipeline = namedtuple("pipeline", "ref status id created_at web_url sha")
Issue = namedtuple("issue", "id title labels state updated_at")
MergeRequest = namedtuple(
    "mergerequest", "state source_branch target_branch author created_at"
)
Milestone = namedtuple(
    "milestone", "title iid state description start_date due_date expired"
)
Label = namedtuple("label", "name")
Branch = namedtuple("branch", "name")
Interval = namedtuple("interval", "start end")

# Different time stamps for the possibilty to use different times in the tests.
date = datetime.today()
past = datetime.today() - timedelta(days=2, hours=3)
commit_time = datetime.today() - timedelta(hours=5)
commit_time2 = datetime.today() - timedelta(days=7, hours=4)
future = datetime.today() + timedelta(days=2, hours=3)

# The expected results for each function regarding the GitLab handlers.
COMMITS_EXPECTED_RESULT_TABLE = Table(
    [
        TableColumn("Time", TableColumnType.TIME),
        TableColumn("Author", TableColumnType.STRING),
        TableColumn("Message", TableColumnType.STRING),
    ],
    [
        [
            unix_timestamp(
                datetime.strptime(date.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")
            ),
            "henak781",
            "Jag är inte i denna grupp",
        ],
        [
            unix_timestamp(
                datetime.strptime(
                    commit_time.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            ),
            "ernla111",
            "Add comment to fail pipeline",
        ],
        [
            unix_timestamp(
                datetime.strptime(
                    commit_time2.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            ),
            "huglu892",
            "Add namedtuple",
        ],
    ],
)

COMMITS_EXPECTED_RESULT_TIMESERIES = TimeSeries(
    [
        [
            1,
            unix_timestamp(
                datetime.strptime(date.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")
            ),
        ],
        [
            1,
            unix_timestamp(
                datetime.strptime(
                    commit_time.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            ),
        ],
        [
            1,
            unix_timestamp(
                datetime.strptime(
                    commit_time2.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            ),
        ],
    ]
)

MERGE_REQUESTS_EXPECTED_RESULT = Table(
    [
        TableColumn("Status", TableColumnType.STRING),
        TableColumn("Source branch", TableColumnType.STRING),
        TableColumn("Target branch", TableColumnType.STRING),
        TableColumn("Author", TableColumnType.STRING),
        TableColumn("Created at", TableColumnType.TIME),
    ],
    [
        ["Open", "testing/adapters", "main", "isagr354", date],
        ["Merged", "feature/product", "main", "huglu892", date],
        ["Open", "feature/html", "main", "adasu264", date],
    ],
)

PIPELINES_EXPECTED_RESULT = Table(
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
                datetime.strptime(date.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")
            ),
            "main",
            "passed",
            6001,
            "huglu892",
            "https://gitlab.se/company/6001",
        ],
        [
            unix_timestamp(
                datetime.strptime(date.isoformat() + "+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")
            ),
            "feature/schedule",
            "running",
            6002,
            "huglu892",
            "https://gitlab.se/company/6002",
        ],
    ],
)

ISSUES_EXPECTED_RESULT = Table(
    [
        TableColumn("ID", TableColumnType.NUMERIC),
        TableColumn("title", TableColumnType.STRING),
        TableColumn("labels", TableColumnType.STRING),
        TableColumn("state", TableColumnType.STRING),
        TableColumn("updated_at", TableColumnType.TIME),
    ],
    [
        [23, "Skriva tester", "Doing", "Open", date],
        [24, "Fika", "Doing", "Open", date],
        [202, "Sova", "On hold", "Open", date],
        [26, "Njuta av solen", "Testing", "Open", date],
    ],
)

MILESTONES_EXPECTED_RESULT = Table(
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
            "Leverans",
            4,
            "active",
            "Slutgiltig leverans av produkten",
            date,
            future,
            False,
        ],
        [
            "Programutveckling",
            3,
            "closed",
            "Period för utveckling av systemet",
            past,
            date,
            True,
        ],
        ["Testning", 2, "active", "Skriva tester", past, date, True],
        [
            "Kandidatprojektsskrivning",
            1,
            "active",
            "Tangentbord som smattrar",
            date,
            future,
            False,
        ],
    ],
)

LABELS_EXPECTED_RESULT = {
    "Doing": "Doing",
    "Backlog": "Backlog",
    "Sprint Backlog": "Sprint Backlog",
    "On hold": "On hold",
}
BRANCHES_EXPECTED_RESULT = {
    "main": "main",
    "testing/everything": "testing/everything",
    "feature/visualize": "feature/visualize",
    "docs/Grafana": "docs/Grafana",
    "fix/pipeline": "fix/pipeline",
}

# The expected results for each function regarding the company handlers.
SALARIES_EXPECTED_RESULT = Table(
    [
        TableColumn("Time", TableColumnType.TIME),
        TableColumn("Company", TableColumnType.STRING),
        TableColumn("Salary", TableColumnType.NUMERIC),
    ],
    [
        [
            unix_timestamp(datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            "Lenas ost och kyckling",
            13000,
        ],
        [
            unix_timestamp(datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            "Skånska grill & bar",
            10000,
        ],
        [
            unix_timestamp(datetime.strptime(past.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            "Sobuli",
            27000,
        ],
        [
            unix_timestamp(datetime.strptime(past.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            "Lenas ost och kyckling",
            17000,
        ],
    ],
)

ORDERS_EXPECTED_RESULT = Table(
    [
        TableColumn("Time", TableColumnType.TIME),
        TableColumn("Order ID", TableColumnType.NUMERIC),
        TableColumn("Company", TableColumnType.NUMERIC),
        TableColumn("Status", TableColumnType.STRING),
        TableColumn("Paying", TableColumnType.BOOLEAN),
    ],
    [
        [
            unix_timestamp(datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            1,
            "Lenas ost och kyckling",
            "Expired",
            False,
        ],
        [
            unix_timestamp(datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            2,
            "Skånska grill & bar",
            "Delivered",
            False,
        ],
        [
            unix_timestamp(datetime.strptime(past.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")),
            3,
            "Sobuli",
            "Active",
            True,
        ],
        [
            unix_timestamp(
                datetime.strptime(future.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
            ),
            4,
            "Lena R",
            "Onboarding",
            False,
        ],
    ],
)

SALES_EXPECTED_RESULT = Table(
    [
        TableColumn("Time", TableColumnType.TIME),
        TableColumn("Sales", TableColumnType.NUMERIC),
        TableColumn("Goal", TableColumnType.NUMERIC),
    ],
    [
        [
            unix_timestamp(
                datetime.strptime(
                    date.isoformat(),
                    "%Y-%m-%dT%H:%M:%S.%f",
                )
            ),
            100000,
            250000,
        ]
    ],
)

TIPS_EXPECTED_RESULT = Table(
    [
        TableColumn("Time", TableColumnType.TIME),
        TableColumn("Tips", TableColumnType.NUMERIC),
    ],
    [
        [
            unix_timestamp(
                datetime.strptime(
                    date.isoformat(),
                    "%Y-%m-%dT%H:%M:%S.%f",
                )
            ),
            12750,
        ]
    ],
)

COMPANIES_EXPECTED_RESULT = {
    "Sobuli": 1,
    "Lenas ost och kyckling": 2,
    "Skånska grill & bar": 3,
    "Lena R": 4,
    "Kalle's Musteri": 5,
}


class MockGitLab:
    """
    This class mocks a GitLab API with all the components that are requested
    in adapters/gitlab.py.

    """

    def __init__(self):
        self.projects = Project(
            lambda project_id: namedtuple(
                "project",
                "commits pipelines mergerequests issues milestones labels branches",
            )(
                namedtuple("commits", "list get")(
                    lambda ref_name, all, since, until: [
                        Commit(
                            date.isoformat() + "+02:00",
                            date.isoformat() + "+02:00",
                            "henak781",
                            "Jag är inte i denna grupp",
                        ),
                        Commit(
                            date.isoformat() + "+02:00",
                            commit_time.isoformat() + "+02:00",
                            "ernla111",
                            "Add comment to fail pipeline",
                        ),
                        Commit(
                            date.isoformat() + "+02:00",
                            commit_time2.isoformat() + "+02:00",
                            "huglu892",
                            "Add namedtuple",
                        ),
                    ],
                    lambda *_: namedtuple("author", "author_name")("huglu892"),
                ),
                namedtuple("pipelines", "list")(
                    lambda all, updated_after, updated_before, ref: [
                        Pipeline(
                            "main",
                            "passed",
                            6001,
                            date.isoformat() + "+02:00",
                            "https://gitlab.se/company/6001",
                            4,
                        ),
                        Pipeline(
                            "feature/schedule",
                            "running",
                            6002,
                            date.isoformat() + "+02:00",
                            "https://gitlab.se/company/6002",
                            4,
                        ),
                    ]
                ),
                namedtuple("mergerequests", "list")(
                    lambda state, ref, updated_after, updated_before, all: [
                        MergeRequest(
                            "Open",
                            "testing/adapters",
                            "main",
                            {"name": "isagr354"},
                            date,
                        ),
                        MergeRequest(
                            "Merged",
                            "feature/product",
                            "main",
                            {"name": "huglu892"},
                            date,
                        ),
                        MergeRequest(
                            "Open", "feature/html", "main", {"name": "adasu264"}, date
                        ),
                    ]
                ),
                namedtuple("issues", "list")(
                    lambda all, labels, state, updated_after, updated_before: [
                        Issue(23, "Skriva tester", "Doing", "Open", date),
                        Issue(24, "Fika", "Doing", "Open", date),
                        Issue(202, "Sova", "On hold", "Open", date),
                        Issue(26, "Njuta av solen", "Testing", "Open", date),
                    ]
                ),
                namedtuple("milestones", "list")(
                    lambda state: [
                        Milestone(
                            "Leverans",
                            4,
                            "active",
                            "Slutgiltig leverans av produkten",
                            date,
                            future,
                            False,
                        ),
                        Milestone(
                            "Programutveckling",
                            3,
                            "closed",
                            "Period för utveckling av systemet",
                            past,
                            date,
                            True,
                        ),
                        Milestone(
                            "Testning", 2, "active", "Skriva tester", past, date, True
                        ),
                        Milestone(
                            "Kandidatprojektsskrivning",
                            1,
                            "active",
                            "Tangentbord som smattrar",
                            date,
                            future,
                            False,
                        ),
                    ]
                ),
                namedtuple("labels", "list")(
                    lambda *_: [
                        Label("Doing"),
                        Label("Backlog"),
                        Label("Sprint Backlog"),
                        Label("On hold"),
                    ]
                ),
                namedtuple("branches", "list")(
                    lambda *_: [
                        Branch("main"),
                        Branch("testing/everything"),
                        Branch("feature/visualize"),
                        Branch("docs/Grafana"),
                        Branch("fix/pipeline"),
                    ]
                ),
            )
        )


class GitlabMetricsAdapterTests(TestCase):
    """
    The purpose of this class is to supply testcases
    for the class GitlabMetricsAdapter in adapters/gitlab.py

    """

    def test_commits_table(self):
        """
        Tests that all commits are retrieved in a table and that the
        format of the table is correct.
        """
        payload = {"project": 20345}
        interval = Interval(past, date)
        gitlab = MockGitLab()
        gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
        function_result = gitlab_metrics_adapter.commits(payload, interval)
        for i in range(len(function_result.columns)):
            assert (
                function_result.columns[i].name
                == COMMITS_EXPECTED_RESULT_TABLE.columns[i].name
            )
            assert (
                function_result.columns[i].type
                == COMMITS_EXPECTED_RESULT_TABLE.columns[i].type
            )
        for row in function_result.rows:
            assert len(row) == len(function_result.columns)
        assert function_result.rows == COMMITS_EXPECTED_RESULT_TABLE.rows

    def test_commits_timeseries(self):
        """
        Tests that all commits are returned as a TimeSeries when this is desired.
        """
        payload = {"project": 20345, "timeseries": True}
        interval = Interval(past, date)
        gitlab = MockGitLab()
        gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
        function_result = gitlab_metrics_adapter.commits(payload, interval)
        assert function_result.data == COMMITS_EXPECTED_RESULT_TIMESERIES.data

    def test_merge_requests(self):
        """
        Tests that all merge requests are retrieved in a table and that the
        format of the table is correct.
        """
        payload = {"project": 20345}
        interval = Interval(past, date)
        gitlab = MockGitLab()
        gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
        function_result = gitlab_metrics_adapter.merge_requests(payload, interval)
        for i in range(len(function_result.columns)):
            assert (
                function_result.columns[i].name
                == MERGE_REQUESTS_EXPECTED_RESULT.columns[i].name
            )
            assert (
                function_result.columns[i].type
                == MERGE_REQUESTS_EXPECTED_RESULT.columns[i].type
            )
        for row in function_result.rows:
            assert len(row) == len(function_result.columns)
        assert function_result.rows == MERGE_REQUESTS_EXPECTED_RESULT.rows

    def test_all_pipelines(self):
        """
        Tests that all pipelines are retrieved in a table and that the
        format of the table is correct.
        """
        payload = {"project": 21345}
        interval = Interval(past, date)
        gitlab = MockGitLab()
        gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
        function_result = gitlab_metrics_adapter.pipelines(payload, interval)
        for i in range(len(function_result.columns)):
            assert (
                function_result.columns[i].name
                == PIPELINES_EXPECTED_RESULT.columns[i].name
            )
            assert (
                function_result.columns[i].type
                == PIPELINES_EXPECTED_RESULT.columns[i].type
            )
        for row in function_result.rows:
            assert len(row) == len(function_result.columns)
        assert function_result.rows == PIPELINES_EXPECTED_RESULT.rows

    def test_issues(self):
        """
        Tests that all issues are retrieved in a table and that the
        format of the table is correct.
        """
        payload = {"project": 20345, "state": "Open"}
        interval = Interval(past, date)
        gitlab = MockGitLab()
        gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
        function_result = gitlab_metrics_adapter.issues(payload, interval)
        for i in range(len(function_result.columns)):
            assert (
                function_result.columns[i].name
                == ISSUES_EXPECTED_RESULT.columns[i].name
            )
            assert (
                function_result.columns[i].type
                == ISSUES_EXPECTED_RESULT.columns[i].type
            )
        for row in function_result.rows:
            assert len(row) == len(function_result.columns)
        assert function_result.rows == ISSUES_EXPECTED_RESULT.rows

    def test_milestones(self):
        """
        Tests that all milestones are retrieved in a table and that the
        format of the table is correct.
        """
        payload = {"project": 21345, "state": "Open"}
        gitlab = MockGitLab()
        gitlab_metrics_adapter = GitLabMetricsAdapter(gitlab)
        function_result = gitlab_metrics_adapter.milestones(payload)
        for i in range(len(function_result.columns)):
            assert (
                function_result.columns[i].name
                == MILESTONES_EXPECTED_RESULT.columns[i].name
            )
            assert (
                function_result.columns[i].type
                == MILESTONES_EXPECTED_RESULT.columns[i].type
            )
        for row in function_result.rows:
            assert len(row) == len(function_result.columns)
        assert function_result.rows == MILESTONES_EXPECTED_RESULT.rows


class GitlabVariablesAdapterTests(TestCase):
    """
    The purpose of this class is to supply testcases
    for the class GitlabVariablesAdapter in adapters/gitlab.py

    """

    def test_labels(self):
        """
        Tests that all labels are retrived and returned correctly in a dictionary.
        """
        data = {"project": 20345}
        gitlab = MockGitLab()
        gitlab_variables_adapter = GitLabVariablesAdapter(gitlab)
        function_result = gitlab_variables_adapter.labels(data)
        assert function_result == LABELS_EXPECTED_RESULT

    def test_branches(self):
        """
        Tests that all branches are retrived and returned correctly in a dictionary.
        """
        data = {"project": 21345}
        gitlab = MockGitLab()
        gitlab_variables_adapter = GitLabVariablesAdapter(gitlab)
        function_result = gitlab_variables_adapter.branches(data)
        assert function_result == BRANCHES_EXPECTED_RESULT
