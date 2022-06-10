# Payload

Some queries to Vision Control require a `Payload` to properly return data. A payload is a JSON object containing parameters and other information specifying what data to return for a given metric.

![Payload](img/payload.png)

!!! Note
    Metrics in Vision Control are separated into a `scope` (original data source that Vision Control relays) and a `target` (the actual metric name). For example, the metric `gitlab-commits` has scope `gitlab` and target `commits`.

!!! example
    Consider a query to the metric `gitlab-commits`.

    If no payload is provided, Vision Control has no way of knowing which project or branch to fetch commits from. This is specified by providing the following payload:

    `{"payload": { "project": 28931, "branch": "feature/cool-stuff"}}`

### Reference

| Key     | Type  | Default | Metrics |
|---------|:-----:|:-------:|--------------------|
| project | `int` | ⚠️[^1]   | *Required*: <ul><li>`gitlab-commits`</li><li>`gitlab-issues`</li> <li>`gitlab-merge_requests`</li><li>`gitlab-pipelines`</li></ul>      |
| branch | `str`  | `main`   | *Optional*:<ul><li>`gitlab-commits`</li><li>`gitlab-issues`</li> <li>`gitlab-merge_requests`</li></ul> |
| labels | `str[]` |         | *Optional*: <ul><li>`gitlab-issues`</li></ul>|

[^1]: Configured with [environment variables](setup.md#environment-variables).
