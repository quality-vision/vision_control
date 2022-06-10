import json
import logging
from datetime import datetime
from collections import namedtuple

log = logging.getLogger(__name__)

from .types import Table, TimeSeries
from ..utils import maybe_pluralize
from .exceptions import (
    PayloadInvalidError,
    ScopeDoesNotExistError,
    ProjectDoesNotExistError,
    TagValuesKeyMissingError,
    CallbackDoesNotExistError,
    MetricsDataKeyMissingError,
    TagValuesInvalidValueError,
    MetricsQueryKeyMissingError,
    MetricsDataInvalidValueError,
    MetricsQueryInvalidValueError,
)


class GrafanaJSONDatasource:
    """The purpose of this class is to serve as a layer that handles the data
    from a HTTP request. It contains two predefined dictionaries with metrics and variables.

    This class only handles what information to retreive depending on the request and then
    compiles the retrieved data into "wished" format and returns it.

    It is closely related to adapters.py.

    What is a scope? : A scope is as set of metrics belonging together.

    Example: GitLab(Category) has commits and users(quantity).
    Therefore GitLabs scope will be commits and users. These quantities, called targets contains links to the gitlab_adapter.

    what is a tag? : A tag is a search value.

    The major functions of this class mirrors the naming scheme of the endpoints required by the Grafana JSON Datasource plugin.
    """

    def __init__(self):
        self.metric_callbacks = {}
        self.tag_callbacks = {}
        self.variable_callbacks = {}

    @property
    def metrics(self):
        result = []

        for scope in self.metric_callbacks.keys():
            for metric in self.metric_callbacks[scope].keys():
                result.append(f"{scope}-{metric}")

        return result

    def add_metrics(self, scope: str, metrics: dict):
        try:
            self.metric_callbacks[scope].update(metrics)
        except KeyError:
            self.metric_callbacks[scope] = metrics

        log.debug(
            f"Added {len(metrics)} {maybe_pluralize(len(metrics), 'metric', 'metrics')} to scope {scope}."
        )

    def add_variables(self, scope: str, variables: dict):
        try:
            self.variable_callbacks[scope].update(variables)
        except KeyError:
            self.variable_callbacks[scope] = variables

        log.debug(
            f"Added {len(variables)} {maybe_pluralize(len(variables), 'variable', 'variables')} to scope {scope}."
        )

    def query(self, data):
        """Extracts queries from data (body of a request) and goes through all of these individual querys.
        depending on the data a callback is created from a specific target and can retrive corresponding data
        builds a time series or a table depending on the callback and appends to the result
        Returns a result in the form of time series and/or tables depending on data and how many querys existed
        """
        result = []
        queries = data.get("targets", [])

        try:
            time_range = data["range"]
        except KeyError:
            raise MetricsDataKeyMissingError("range")

        try:
            time_start = time_range["from"]
        except KeyError:
            raise MetricsDataInvalidValueError("range", "from")

        try:
            time_end = time_range["to"]
        except KeyError:
            raise MetricsDataInvalidValueError("range", "to")

        interval = namedtuple("interval", "start end")(
            datetime.strptime(time_start, "%Y-%m-%dT%H:%M:%S.%f%z"),
            datetime.strptime(time_end, "%Y-%m-%dT%H:%M:%S.%f%z"),
        )

        for query in queries:
            identifier = query.get("target")
            if not identifier:
                raise MetricsQueryKeyMissingError("target")

            reference = query.get("refId")
            if not reference:
                raise MetricsQueryKeyMissingError("refId")

            try:
                scope, metric = identifier.split("-")
            except ValueError:
                raise MetricsQueryInvalidValueError("target", identifier)

            metrics = self.metric_callbacks.get(scope)
            if not metrics:
                raise ScopeDoesNotExistError(f"'{scope}' is not a valid scope.")

            callback = metrics.get(metric)
            if not callback:
                raise CallbackDoesNotExistError(scope, metric)

            payload = query.get("payload", {})
            if isinstance(payload, str):
                payload = {}

            try:
                response_data = callback(payload, interval)
            except (PayloadInvalidError, ProjectDoesNotExistError) as err:
                raise err

            result.append(self._build_result(reference, identifier, response_data))

        return result

    def _build_result(self, reference, identifier, data):
        """Format response data from adapters how Grafana want it."""

        match data:
            case Table(columns=columns, rows=rows):
                log.debug(
                    f"Returning table with {len(rows)} {maybe_pluralize(len(rows), 'row', 'rows')}."
                )

                return {
                    "refId": reference,
                    "columns": [
                        {"text": column.name, "type": column.type.value}
                        for column in columns
                    ],
                    "rows": rows,
                    "type": "table",
                }

            case TimeSeries(data=data):
                log.debug(
                    f"Returning timeseries with {len(data)} {maybe_pluralize(len(data), 'datapoint', 'datapoints')}."
                )
                return {
                    "refId": reference,
                    "target": identifier,
                    "datapoints": data,
                }

        raise TypeError(f"'{type(data)} is not a valid response data type.'")

    def search(self):
        """Returns all available metrics"""
        return self.metrics

    def variable(self, data):
        """Returns options for a variable"""
        payload = data.get("payload")
        target = json.loads(payload.get("target"))

        scope, variable, variable_data = (
            target.get("scope"),
            target.get("variable"),
            target.get("data", {}),
        )
        variables = self.variable_callbacks.get(scope)
        if not variables:
            raise ScopeDoesNotExistError(f"'{scope}' is not a valid scope.")

        callback = variables.get(variable)
        if not callback:
            raise CallbackDoesNotExistError(scope, variable)
        result = callback(variable_data)
        return [{"__text": key, "__value": value} for key, value in result.items()]
