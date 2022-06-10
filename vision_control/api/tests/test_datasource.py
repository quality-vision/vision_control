from django.test import TestCase

from datetime import datetime

import pytest

from ..utils import unix_timestamp
from ..grafana_json_datasource.types import Table, TableColumn, TableColumnType
from ..grafana_json_datasource.datasource import GrafanaJSONDatasource
from ..grafana_json_datasource.exceptions import *

date = datetime.today()


class DataMocker:
    """
    The purpose of this class is to mock data needed for variables() and query().
    """

    def __init__(self):
        pass

    def mock_variables(self, *_):
        """
        Mocks data for the variables
        """
        return {
            "Company Utveckling": 10293,
            "Company ny feature": 20394,
        }

    def mock_metrics(self, *_):
        """
        Mocks data for the queries
        """
        return Table(
            [
                TableColumn("Time", TableColumnType.TIME),
                TableColumn("Author", TableColumnType.STRING),
                TableColumn("Message", TableColumnType.STRING),
            ],
            [
                [
                    unix_timestamp(
                        datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                    ),
                    "agnfr874",
                    "Fak yu jag tar examen snart",
                ],
                [
                    unix_timestamp(
                        datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                    ),
                    "marhu057",
                    "Ja: E-type är min pappa",
                ],
                [
                    unix_timestamp(
                        datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                    ),
                    "ivaka037",
                    "tai iš tikrųjų tikras lietuvis",
                ],
            ],
        )

    def wrong_data_type(self, *_):
        """
        Mocks data for the queries with wrong data type
        """
        return {"Company": "commits"}


class GrafanaJSONDataTests(TestCase):
    """
    The purpose of this class is to supply test cases for grafana_json_datasource/datasource.py
    """

    def test_add_metrics(self):
        """
        Tests that metrics are added correctly and that the scopes are updated
        when a new metrics is added.
        """
        metrics = [
            "GitLab-users",
            "GitLab-commits",
            "Company-companies",
            "Company-staff",
        ]
        datasource = GrafanaJSONDatasource()
        datasource.add_metrics(
            "GitLab",
            {"users": ["henak781", "adasu264"], "commits": ["3fecefe", "65hgafs6h"]},
        )
        datasource.add_metrics(
            "Company",
            {"companies": ["Sobuli", "Goolio"], "staff": ["henak781", "ernla111"]},
        )
        assert datasource.search() == metrics
        metrics.append("Company-orders")
        datasource.add_metrics("Company", {"orders": [1238947352, 3425161]})
        assert datasource.search() == metrics

    def test_add_variables(self):
        """
        Tests that variables are added correctly and that the scopes are updated
        when a new variable is added.
        """
        datasource = GrafanaJSONDatasource()
        mocker = DataMocker()

        result = [
            {"__text": "Company Utveckling", "__value": 10293},
            {"__text": "Company ny feature", "__value": 20394},
        ]
        data = {
            "payload": {"target": '{"scope": "gitlab",  "variable": "projects"}'},
            "range": {
                "from": "2022-04-26T03:12:39.295Z",
                "to": "2022-04-26T09:12:39.295Z",
                "raw": {"from": "now-6h", "to": "now"},
            },
        }
        datasource.add_variables(
            "gitlab",
            {"projects": mocker.mock_variables},
        )
        assert datasource.variable(data) == result

    def test_variable_no_scope(self):
        """
        Sends data with a scope that does not exist and checks that the correct error is raised.

        """
        data = {
            "payload": {"target": '{"scope": "gitlab",  "variable": "projects"}'},
            "range": {
                "from": "2022-04-26T03:12:39.295Z",
                "to": "2022-04-26T09:12:39.295Z",
                "raw": {"from": "now-6h", "to": "now"},
            },
        }
        datasource = GrafanaJSONDatasource()
        datasource.add_variables("Company", {"staff": ["henak781", "robek274"]})
        with pytest.raises(ScopeDoesNotExistError):
            datasource.variable(data)

    def test_variable_no_callback(self):
        """
        Sends data with a variable the scope does not have and checks that the correct error is raised.

        """
        datasource = GrafanaJSONDatasource()
        data = {
            "payload": {
                "target": '{"scope": "gitlab",  "variable": "projects", "data": {"id": 20345}}'
            },
            "range": {
                "from": "2022-04-26T03:12:39.295Z",
                "to": "2022-04-26T09:12:39.295Z",
                "raw": {"from": "now-6h", "to": "now"},
            },
        }
        datasource.add_variables("gitlab", {"users": ["henak781", "robek274"]})
        with pytest.raises(CallbackDoesNotExistError):
            datasource.variable(data)

    def test_query(self):
        """
        Tests that a query with correct data can be made.
        """
        datasource = GrafanaJSONDatasource()
        mocker = DataMocker()
        datasource.add_metrics("gitlab", {"commits": mocker.mock_metrics})
        data = {
            "app": "dashboard",
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
            },
            "targets": [
                {
                    "refId": "A",
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab-commits",
                }
            ],
        }

        result = [
            {
                "refId": "A",
                "columns": [
                    {"text": "Time", "type": "time"},
                    {"text": "Author", "type": "string"},
                    {"text": "Message", "type": "string"},
                ],
                "rows": [
                    [
                        unix_timestamp(
                            datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                        ),
                        "agnfr874",
                        "Fak yu jag tar examen snart",
                    ],
                    [
                        unix_timestamp(
                            datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                        ),
                        "marhu057",
                        "Ja: E-type är min pappa",
                    ],
                    [
                        unix_timestamp(
                            datetime.strptime(date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                        ),
                        "ivaka037",
                        "tai iš tikrųjų tikras lietuvis",
                    ],
                ],
                "type": "table",
            }
        ]
        assert datasource.query(data) == result

    def test_query_wrong_data_type(self):
        """
        Makes a query that returns the result in a dict instead of table or timeseries
        and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        mocker = DataMocker()
        datasource.add_metrics("gitlab", {"commits": mocker.wrong_data_type})
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
            },
            "targets": [
                {
                    "refId": "A",
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab-commits",
                }
            ],
        }
        with pytest.raises(TypeError):
            datasource.query(data)

    def test_query_no_range(self):
        """
        Makes a query with data that misses a range and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "timeInfo": "",
            "interval": "20s",
            "intervalMs": 20000,
            "targets": [
                {
                    "refId": "A",
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab-commits",
                }
            ],
        }

        with pytest.raises(MetricsDataKeyMissingError):
            datasource.query(data)

    def test_query_no_timerange(self):
        """
        Makes a query with data that misses starttime on its range and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "range": {
                "to": "2022-04-26T09:22:11.365Z",
                "raw": {"from": "now-7d", "to": "now"},
            },
            "timeInfo": "",
            "interval": "20s",
            "intervalMs": 20000,
            "targets": [
                {
                    "refId": "A",
                    "datasource": {
                        "type": "simpod-json-datasource",
                        "uid": "tU5oHYQnz",
                    },
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab-commits",
                }
            ],
            "maxDataPoints": 960,
            "scopedVars": {
                "Project": {"text": "Company Utveckling", "value": "10293"},
                "branch": {"text": "main", "value": "main"},
                "__interval": {"text": "20s", "value": "20s"},
                "__interval_ms": {"text": "20000", "value": 20000},
            },
            "startTime": 1650964931365,
            "rangeRaw": {"from": "now-7d", "to": "now"},
            "adhocFilters": [],
        }

        with pytest.raises(MetricsDataInvalidValueError):
            datasource.query(data)

    def test_query_no_target(self):
        """
        Makes a query with data that misses a target and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
                "raw": {"from": "now-7d", "to": "now"},
            },
            "targets": [
                {"refId": "A", "payload": {"project": "10293", "branch": "main"}}
            ],
        }

        with pytest.raises(MetricsQueryKeyMissingError):
            datasource.query(data)

    def test_query_no_ref_id(self):
        """
        Makes a query with data that misses a refId and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
                "raw": {"from": "now-7d", "to": "now"},
            },
            "targets": [
                {
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab-commits",
                }
            ],
        }

        with pytest.raises(MetricsQueryKeyMissingError):
            datasource.query(data)

    def test_query_invalid_target(self):
        """
        Makes a query with a target that does not exist and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        datasource.add_metrics(
            "GitLab",
            {"users": ["henak781", "adasu264"], "commits": ["3fecefe", "65hgafs6h"]},
        )
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
                "raw": {"from": "now-7d", "to": "now"},
            },
            "targets": [
                {
                    "refId": "A",
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab_commits",
                }
            ],
        }

        with pytest.raises(MetricsQueryInvalidValueError):
            datasource.query(data)

    def test_query_invalid_scope(self):
        """
        Makes a query with an incorrect scope in the target and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        datasource.add_metrics("Company", {"orders": [1238947352, 3425161]})
        data = {
            "app": "dashboard",
            "requestId": "Q231",
            "timezone": "browser",
            "panelId": 6,
            "dashboardId": None,
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
                "raw": {"from": "now-7d", "to": "now"},
            },
            "timeInfo": "",
            "interval": "20s",
            "intervalMs": 20000,
            "targets": [
                {
                    "refId": "A",
                    "datasource": {
                        "type": "simpod-json-datasource",
                        "uid": "tU5oHYQnz",
                    },
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "huglu892_grammatikskola-orders",
                }
            ],
            "maxDataPoints": 960,
            "scopedVars": {
                "Project": {"text": "Company Utveckling", "value": "10293"},
                "branch": {"text": "main", "value": "main"},
                "__interval": {"text": "20s", "value": "20s"},
                "__interval_ms": {"text": "20000", "value": 20000},
            },
            "startTime": 1650964931365,
            "rangeRaw": {"from": "now-7d", "to": "now"},
            "adhocFilters": [],
        }
        with pytest.raises(ScopeDoesNotExistError):
            datasource.query(data)

    def test_query_no_callback(self):
        """
        Makes a query with incorrect metric for the scope so that a callback is not
        possible and makes sure that the correct error is raised.
        """
        datasource = GrafanaJSONDatasource()
        datasource.add_metrics(
            "gitlab",
            {"users": ["henak781", "adasu264"], "commits": ["3fecefe", "65hgafs6h"]},
        )
        data = {
            "range": {
                "from": "2022-04-19T09:22:11.365Z",
                "to": "2022-04-26T09:22:11.365Z",
                "raw": {"from": "now-7d", "to": "now"},
            },
            "targets": [
                {
                    "refId": "A",
                    "payload": {"project": "10293", "branch": "main"},
                    "target": "gitlab-merges",
                }
            ],
        }
        with pytest.raises(CallbackDoesNotExistError):
            datasource.query(data)
