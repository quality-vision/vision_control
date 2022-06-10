# API

Vision Control provides a REST API. It is primarly designed to implement the endpoints required by [JSON API Grafana Datasource plugin](../grafana/resources.md#json-api-grafana-datasource). Of course, it can be adapted to work with more tools as well.

## Authentication

!!! warning
      At the moment, Vision Control has no support for authentication.

During development Grafana and Vision Control were run on the same [Docker Network](https://docs.docker.com/network/), which meant that they were able to communicate with each other without exposing Vision Control to the outside world.

For remote access [caddy-docker-proxy](https://github.com/lucaslorentz/caddy-docker-proxy) was used to provide an authenticated reverse-proxy. Because Vision Control potentially contains sensitive or secret information, it is recommended to use a more sophisticated mechanism if it needs to be exposed.

## Endpoints

### Status

Verify that Vision Control is running correctly.

```
GET /api/
```

**Example request:**

```shell
$ curl --request GET "https://vision_control.example.com/api/"
```

**Example response:**

```json
HTTP/2 200 OK
```

### Search

Return a list of all available metrics.

```
GET /search
```

**Example request:**

```shell
$ curl --request GET "https://vision_control.example.com/api/search"
```

**Example response:**

```json
[
   "gitlab-commits",
   "gitlab-users",
   "gitlab-pipelines",
   "gitlab-issues",
   "gitlab-merge_requests",
   "gitlab-milestones",
   "vision_control-version"
]
```


### Query

Return data for a given metric.

```
POST /api/query
```

| Attribute | Type   | Required | Description                   |
|-----------|:------:|:--------:|-------------------------------|
| `range`   | `json` | yes      | Date range for data that is returned. |
| `range.from`   | `date` | yes      | Start of date range. |
| `range.to`   | `date` | yes      | End of date range. |
| `targets` | `json[]` | yes | Array of Grafana queries. |
| `targets[i].refId` | `string` | yes | Request-unique query identifier. |
| `targets[i].target` | `string` | yes | Metric name to query. [^1]  |
| `targets[i].payload` | `string`/`json` | yes | Metric query [payload](payload.md). |

Body should contain a valid Grafana query according to the [plugin specification](https://github.com/simPod/GrafanaJsonDatasource#query).

An invalid query will be answered with an appropriate HTTP status code together with a description of the problem.

**Example request:**

```shell
$ curl --request GET "https://vision_control.example.com/api/query" --header "Content-Type: application/json" --data {...}
```

!!! note
      The example data contains additional attributes added by Grafana, outside of what is required.

```json
{
   "app":"explore",
   "dashboardId":0,
   "timezone":"browser",
   "startTime":1653028603030,
   "interval":"2s",
   "intervalMs":2000,
   "panelId":"Q-60e0331d-a84f-4809-a4e2-ca1b5e9ebd06-0",
   "targets": [
      {
         "refId":"A",
         "key":"Q-60e0331d-a84f-4809-a4e2-ca1b5e9ebd06-0",
         "payload":"",
         "target":"vision_control-version",
         "datasource":{
            "type":"simpod-json-datasource",
            "uid":"P4136969F2C9A4A00"
         }
      }
   ],
   "range":{
      "from":"2022-05-20T05:36:43.025Z",
      "to":"2022-05-20T06:36:43.025Z",
      "raw":{
         "from":"now-1h",
         "to":"now"
      }
   },
   "requestId":"explore_left",
   "rangeRaw":{
      "from":"now-1h",
      "to":"now"
   },
   "scopedVars":{
      "__interval":{
         "text":"2s",
         "value":"2s"
      },
      "__interval_ms":{
         "text":2000,
         "value":2000
      }
   },
   "maxDataPoints":1828,
   "liveStreaming":false,
   "adhocFilters":[

   ]
}
```

**Example response:**

```json
[
   {
      "refId":"A",
      "columns":[
         {
            "text":"version",
            "type":"string"
         }
      ],
      "rows":[
         [
            "d2890a1"
         ]
      ],
      "type":"table"
   }
]
```

### Variable

Return all options for a given variable.

```
GET /api/variable
```

| Attribute | Type   | Required | Description                   |
|-----------|:------:|:--------:|-------------------------------|
| `range`   | `json` | yes      | Date range for data that is returned. |
| `range.from`   | `date` | yes      | Start of date range. |
| `range.to`   | `date` | yes      | End of date range. |
| `payload.target`   | `string` | yes   | Variable query payload.[^2] `target` is expected to be inside `payload` as its only attribute to comform to Grafana's calling conventions.  |
| `payload.target.scope` | `string` | yes   | Variable scope. For example, `gitlab`.|
| `payload.target.variable` | `string` | yes   | Variable name. For example, `branches`.|
| `payload.target.data` | `string` | no   | Additional context-specific data passed to adapter handling the variable. |

An invalid query will be answered with an appropriate HTTP status code together with a description of the problem.

**Example request:**

```shell
$ curl --request GET "https://vision_control.example.com/api/variable" --header "Content-Type: application/json" --data {...}
```

```json
{
   "payload":{
      "target":"{\"scope\": \"gitlab\", \"variable\": \"branches\", \"data\": {\"project\": 23021}}"
   },
   "range":{
      "from":"2022-04-20T11:50:13.114Z",
      "to":"2022-05-20T11:50:13.114Z",
      "raw":{
         "from":"now-30d",
         "to":"now"
      }
   }
}
```

**Example response:**

!!! note
      This format may look a bit weird, but must be that way for Grafana to be able to interpret it. `__text` is what will be shown in the interface and `__value` is its actual value.

```json
[
   {
      "__text":"api_comments",
      "__value":"api_comments"
   },
   {
      "__text":"docs/api",
      "__value":"docs/api"
   },
   {
      "__text":"docs/grafana-trix",
      "__value":"docs/grafana-trix"
   },
   {
      "__text":"docs/shared-objects",
      "__value":"docs/shared-objects"
   }
]
```

### GitLab Hook

Return data for a given metric.

```
POST /hooks/gitlab
```

| Attribute | Type   | Required | Description                   |
|-----------|:------:|:--------:|-------------------------------|
| `HTTP_X_GITLAB_TOKEN` | HTTP header | yes | Used to verify that the request comes from a known place. |
| Request body | `json` | yes | Data for a [GitLab webhook](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html). |

An invalid query will be answered with an appropriate HTTP status code together with a description of the problem.

!!! warning
      This is an internal endpoint that shouldn't be called on its own. GitLab will be configured on system startup to call this endpoint on webhooks – without any manual work from your side.

[^1]: Must be on format [`(?<scope>[A-Za-z]+[A-Za-z_0-9]*)-(?<metric>[A-Za-z]+[A-Za-z_0-9]*)`](https://regex101.com/r/2ywCbg/1), where first part is `scope` and the other is `metric` inside that scope. More information about this can be found [here](payload.md).

[^2]: Same payload as mentioned (referred to as `data`) [here](datasource.md#variables-adapters).
