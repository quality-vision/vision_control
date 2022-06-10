# Gallery

## Dashboards

### GitLab

<img src="../img/GitLab-dashboard.png" width=90%>

{{ render_tags(["gitlab", "scrum", "variables", "commits", "nested variables", "pie chart", "heatmap", "bargraph"]) }}

Vision Control comes with an assembled GitLab dashboard. This dashboard contains panels related to GitLab, such as commits, issues, pipelines and more.

{{ implementation("Variables", ["../img/variable_project.png", "../img/variable_branch.png", "../img/variable_milestonestate.png"]) }}

### Loki

<img src="../img/Loki-dashboard.png" width=90%>

{{ render_tags(["loki", "annotations", "companies", "wage", "successful features", "pie chart", "clock"]) }}

The Loki dashboard has panels related to Loki and shows the application logs in different panels. For example this dashboard visualize feature usage over time and successful features.

{{ implementation("Variables", ["../img/variable_project.png", "../img/variable_feature.png", "../img/annotation_deployments.png"]) }}

### Sentry

<img src="../img/Sentry-dashboard.png" width=90%>

{{ render_tags(["sentry", "transactions", "logs", "errors by type", "events by type", "bar chart", "pie chart", "events by day", "heatmap"]) }}

### Prometheus

<img src="../img/Prometheus-dashboard.png" width=90%>

{{ render_tags(["prometheus", "operating system", "cpu", "usage", "ubuntu", "clock"]) }}

## Panels

Vision Control have a standard panel library with panels that can be reused and modified as needed. The main purpose is to show the different ways panels can be created and how different transforms can be applied to change the structure of the data.

### GitLab

#### Commits

<img src="../img/gitlab_commits.png" width=90%>

{{ render_tags(["gitlab", "commits", "heatmap", "hourly"]) }}

{{ implementation("Hourly heatmap", ["../img/gitlab_commits_implementation.png", "../img/gitlab_commits_implementation2.png", "../img/gitlab_commits_implementation3.png"]) }}

#### Commits by author

<img src="../img/gitlab_commits-by-author.png" width=90%>

{{ render_tags(["gitlab", "commits", "author", "bar chart"]) }}

{{ implementation("Bar chart", ["../img/gitlab_commits-by-author_implementation.png", "../img/gitlab_commits-by-author_implementation2.png", "../img/gitlab_commits-by-author_implementation3.png"]) }}

#### Pipelines

<img src="../img/gitlab_pipelines.png" width=90%>

{{ render_tags(["gitlab", "pipelines", "table"]) }}

{{ implementation("Table", ["../img/gitlab_pipelines_implementation.png", "../img/gitlab_pipelines_implementation2.png"]) }}

#### Failed pipelines

<img src="../img/gitlab_failed-pipelines.png" width=90%>

{{ render_tags(["gitlab", "failed" "pipelines", "stat", "number"]) }}

{{ implementation("Stat", ["../img/gitlab_failed-pipelines_implementation.png", "../img/gitlab_failed-pipelines_implementation2.png"]) }}

#### Last pipeline status

<img src="../img/gitlab_last-pipeline-status.png" width=90%>

{{ render_tags(["gitlab", "pipelines", "status"]) }}

{{ implementation("Stat", ["../img/gitlab_last-pipeline-status_implementation.png", "../img/gitlab_last-pipeline-status_implementation2.png", "../img/gitlab_last-pipeline-status_implementation3.png", "../img/gitlab_last-pipeline-status_implementation4.png"]) }}

#### Merge requests

<img src="../img/gitlab_merge-requests.png" width=90%>

{{ render_tags(["gitlab", "merge requests", "stat", "numbers"]) }}

{{ implementation("Stat", ["../img/gitlab_merge-requests_implementation.png", "../img/gitlab_merge-requests_implementation2.png", "../img/gitlab_merge-requests_implementation3.png", "../img/gitlab_merge-requests_implementation4.png"]) }}

#### Milestones

<img src="../img/gitlab_milestones.png" width=90%>

{{ render_tags(["gitlab", "milestones", "table"]) }}

{{ implementation("Table", ["../img/gitlab_milestones_implementation.png", ]) }}

#### New vs maintenance

<img src="../img/gitlab_new-vs-maintenance.png" width=90%>

{{ render_tags(["gitlab", "issues", "new", "maintenance", "pie chart"]) }}

{{ implementation("Pie chart", ["../img/gitlab_new-vs-maintenance_implemenation.png", "../img/gitlab_new-vs-maintenance_implemenation2.png"]) }}

#### Scrum board issues

<img src="../img/gitlab_scrum-board-issues.png" width=90%>

{{ render_tags(["gitlab", "issues", "scrum-board", "pie chart"]) }}

{{ implementation("Pie chart", ["../img/gitlab_scrum-board-issues_implementation.png", "../img/gitlab_scrum-board-issues_implementation2.png", "../img/gitlab_scrum-board-issues_implementation3.png"]) }}

#### Users

<img src="../img/gitlab_users.png" width=90%>

{{ render_tags(["gitlab", "users", "status", "table"]) }}

{{ implementation("Table", ["../img/gitlab_users_implemenation.png", "../img/gitlab_users_implemenation2.png", "../img/gitlab_users_implemenation3.png"]) }}

### Sentry

#### Errors by type

<img src="../img/sentry_errors-by-type.png" width=90%>

{{ render_tags(["sentry", "errors", "pie chart"]) }}

{{ implementation("Pie chart", ["../img/sentry_errors-by-type_implementation.png", "../img/sentry_errors-by-type_implementation2.png", "../img/sentry_errors-by-type_implementation3.png"]) }}

#### Events by type

<img src="../img/sentry_events-by-type.png" width=90%>

{{ render_tags(["sentry", "events", "bar chart"]) }}

{{ implementation("Bar chart", ["../img/sentry_events-by-type_implementation.png", "../img/sentry_events-by-type_implementation2.png", "../img/sentry_events-by-type_implementation3.png"]) }}

#### Transactions by day

<img src="../img/sentry_transactions-by-day.png" width=90%>

{{ render_tags(["sentry", "transactions", "day" "time series"]) }}

{{ implementation("Time series", ["../img/sentry_transactions-by-day_implementation.png", ]) }}

#### Transactions by hour

<img src="../img/sentry_transactions-by-hour.png" width=90%>

{{ render_tags(["sentry", "transactions", "hour" "heatmap"]) }}

{{ implementation("Hourly heatmap", ["../img/sentry_transactions-by-hour_implementation.png", "../img/sentry_transactions-by-hour_implementation2.png"]) }}

#### Logs

<img src="../img/sentry_logs.png" width=90%>

{{ render_tags(["sentry", "logs"]) }}

{{ implementation("Logs", ["../img/sentry_logs_implementation.png", ]) }}

### Prometheus

#### CPU usage

<img src="../img/prometheus_cpu-usage.png" width=90%>

{{ render_tags(["prometheus", "cpu usage"]) }}

{{ implementation("Logs", ["../img/prometheus_cpu-usage_implementation.png", ]) }}

#### OS version

<img src="../img/prometheus_os-version.png" width=90%>

{{ render_tags(["prometheus", "os version"]) }}

{{ implementation("Logs", ["../img/prometheus_os-version_implementation.png", "../img/prometheus_os-version_implementation2.png"]) }}

## Data sources

How to configure the different datasources.

### Vision Control

<img src="../img/datasource_visioncontrol.png" width=90%>

### Loki

<img src="../img/datasource_loki.png" width=90%>

### Sentry

<img src="../img/datasource_sentry.png" width=90%>

### Prometheus

<img src="../img/datasource_prometheus.png" width=90%>
