from django.conf import settings

from ..grafana_json_datasource import Table, TableColumn, TableColumnType


class VisionControlMetricsAdapter:
    """The purpose of this class is to expose Grafana metrics related to the middleware."""

    def __init__(self):
        pass

    def version(self, *_):
        return Table(
            [TableColumn("version", TableColumnType.STRING)],
            [[settings.GIT_REVISION]],
        )
