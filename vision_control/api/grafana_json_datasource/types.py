from enum import Enum


class TableColumnType(Enum):
    """Available types for a TableColumn."""

    BOOLEAN = "bool"
    JSON = "json"
    NUMERIC = "numeric"
    STRING = "string"
    TIME = "time"


class TableColumn:
    """Column definition of a given type."""

    def __init__(self, name: str, type: TableColumnType):
        self.name = name
        self.type = type


class Table:
    """Table of data."""

    __match_args__ = ("columns", "rows")

    def __init__(self, columns: list[TableColumn], rows):
        self.columns = columns
        self.rows = rows


class TimeSeries:
    """Timeseries of data."""

    __match_args__ = "data"

    def __init__(self, data):
        self.data = data
