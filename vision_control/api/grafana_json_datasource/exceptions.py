class ScopeDoesNotExistError(Exception):
    def __init__(self, scope):
        self.message = f"{scope} is not a valid scope."
        super(ScopeDoesNotExistError, self).__init__(self.message)


class MetricsDataKeyMissingError(Exception):
    def __init__(self, key):
        self.message = f"Missing key in metrics query data: '{key}'"
        super(MetricsDataKeyMissingError, self).__init__(self.message)


class MetricsDataInvalidValueError(Exception):
    def __init__(self, key, value):
        self.message = f"Invalid value for key {key}: '{value}'"
        super(MetricsDataInvalidValueError, self).__init__(self.message)


class MetricsQueryKeyMissingError(Exception):
    def __init__(self, key):
        self.message = f"Missing key in metrics query: '{key}'"
        super(MetricsQueryKeyMissingError, self).__init__(self.message)


class MetricsQueryInvalidValueError(Exception):
    def __init__(self, key, value):
        self.message = f"Invalid value for key {key}: '{value}'"
        super(MetricsQueryInvalidValueError, self).__init__(self.message)


class TagValuesKeyMissingError(Exception):
    def __init__(self, key):
        self.message = f"Missing key in tag values: '{key}'"
        super(TagValuesInvalidValueError, self).__init__(self.message)


class TagValuesInvalidValueError(Exception):
    def __init__(self, key, value):
        self.message = f"Invalid value for key {key}: '{value}'"
        super(TagValuesInvalidValueError, self).__init__(self.message)


class CallbackDoesNotExistError(Exception):
    def __init__(self, scope, target):
        self.message = f"Callback does not exist for {target} in scope {scope}"
        super(CallbackDoesNotExistError, self).__init__(self.message)


class PayloadInvalidError(Exception):
    def __init__(self, target):
        self.message = f"Payload is missing or malformed for target {target}"
        super(PayloadInvalidError, self).__init__(self.message)


class ProjectDoesNotExistError(Exception):
    def __init__(self, project):
        self.message = f"Cannot find project with id {project}"
        super(ProjectDoesNotExistError, self).__init__(self.message)
