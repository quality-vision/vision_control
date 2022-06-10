# Adapters

Adapters are classes that provide a set of methods that map against either metrics or variables in a given scope.
As an example, the metrics adapter for the GitLab scope, GitLabMetricsAdapter, provides methods with names
corresponding to each metric such as `commits()`, `issues()`, `pipelines()`, etc. These map to the
metrics `gitlab-commits`, `gitlab-issues`, and `gitlab-pipelines` respectively.

Sometimes the external data sources you use require additional parameters to function properly such as specifying a
project ID for GitLab repositories. This data can be accessed by unpacking the [payload](payload.md) object.

### Creating new adapters

While Vision Control provides out-of-the-box support for GitLab any additional data sources that lack a native Grafana-plugin 
must be integrated by creating a corresponding adapter in `api/adapters`. It is recommended to study the existing adapters to form an idea of how they work and what they do.

!!! note
    Vision Control provides helper classes in `api/grafana_json_datasource/types.py` to help with data serialization
    when working against Grafana. It is recommended to use these to the extent it is possible for metric adapters.

Once an adapter has been created that fetches data from the desired data source (whether that's a 3rd-party API or
a local mock class), processes it, and repackages it into the appropriate table or time series format, it needs to be
registered as either a metric or variable. This is done in `api/services.py` by instantiating the adapter class and registering
each method along with the corresponding metrics/variables on the datasource object. Here it is again recommended to
study the existing implementation, since registering custom adapters should look more or less the same.

!!! warning
    It is **highly** recommended to ensure that the key string matches the method name for each target in a registered
    metric or variable. Mismatched names are unsupported and may result in bad behavior.
