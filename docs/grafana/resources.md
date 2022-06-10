# Resources

Useful information that we have used to learn more about Grafana and its features is presented here. The information in the links mainly relates to the creation and editing of Grafana dashboards and panels, and further information that relates to it.

## Variables

Variables are created on a dashboard-wide basis. They allow for the user to select a number of pre-defined alternatives to choose from when requesting data. The variables are visible at the top of the dashboard.

* [Variable examples](https://grafana.com/docs/grafana/latest/variables/variable-examples/)
* [Templates and variables](https://grafana.com/docs/grafana/latest/variables/)
* [Variable types](https://grafana.com/docs/grafana/latest/variables/variable-types/)
* [Variable syntax](https://grafana.com/docs/grafana/latest/variables/syntax/)

### Types

These are the different types of variables used in dashboards.

#### Query

The query type is used the most. The possible values of the variable are retrived by queries from the choosen data source. In the example dashboard the variable `$project` is derived by the query:

```json
{
   "scope": "gitlab",
   "variable": "projects"
}
```

This variable retrives all GitLab projects from Vision Control.

##### Nested Variables

Query variables can also be nestled. This means that the query is dependent on one or more other variables. The `$branch` variable in the GitLab dashboard, is a nestled variable dependent on the `$project` variable. By using a nestled variable only the branches for the specific project is available. `$branch` is derived by the query:

```json
{
   "scope": "gitlab",
   "variable": "branches",
   "data": {
      "project": $project
   }
}
```

#### Custom

Custom variables have static predefined values. They are defined in a comma-separated list. In the GitLab example dashboard, `$milestone` is a custom variable. This is because the values are always known and cannot take any other values than `all`, `closed` or `active`.

## Transformations

An important part of data formatting in Grafana is done via transformations. These are functions which change the structure of the data they are applied to and varies greatly in exatly what they do. Transformations can be stacked, which allows for great customisation of how you can visualise your data.

* [About transformations](https://grafana.com/docs/grafana/latest/panels/transform-data/about-transformation/)
* [Transformation functions](https://grafana.com/docs/grafana/latest/panels/transform-data/transformation-functions/)
* [Transform data](https://grafana.com/docs/grafana/latest/panels/transform-data/)

## Requests

When making data requests to Grafana for official plugins, the requested data can either be taken in raw form or be formatted for easier use in panels. This formatting is unique to each request, and as such multiple different formats can be requested on the same panel.

* [Info about expressions](https://grafana.com/docs/grafana/latest/panels/query-a-data-source/use-expressions-to-manipulate-data/about-expressions/)
* [Write an expression](https://grafana.com/docs/grafana/latest/panels/query-a-data-source/use-expressions-to-manipulate-data/write-an-expression/)

## Plugins

We use the built-in core plugins, but also the following plugins from the Grafana plugin directory.

### Hourly heatmap

:fa-home: [Plugin](https://grafana.com/grafana/plugins/marcusolsson-hourly-heatmap-panel) <br>
:fa-github: [Github](https://github.com/marcusolsson/grafana-hourly-heatmap-panel)

Used for visualizing commit made over time.

### JSON API Grafana Datasource

:fa-home: [Source](https://grafana.com/grafana/plugins/simpod-json-datasource) <br>
:fa-github: [Github](https://github.com/simPod/GrafanaJsonDatasource)

The plugin that Vision Control is based on. A fork of [grafana/simple-json-datasource](https://github.com/grafana/simple-json-datasource), which is still a good resource, because the new plugin documentation is minimal.

!!! warning
    The plugin has a new endpoint which we rely on: `/variables`. For some reason it didn't get called before we updated Grafana to version 8.5.

### Loki

[LogQL](https://grafana.com/docs/loki/latest/logql)

### Prometheus

:fa-home: [Plugin](https://grafana.com/grafana/plugins/prometheus)

### Sentry

:fa-home: [Plugin](https://grafana.com/grafana/plugins/grafana-sentry-datasource)

### Singlestat Math

:fa-github: [Github](https://github.com/black-mirror-1/singlestat-math) <br>
:fa-home: [Plugin](https://grafana.com/grafana/plugins/blackmirror1-singlestat-math-panel)

### Static

:fa-home: [Plugin](https://grafana.com/grafana/plugins/marcusolsson-static-datasource) <br>
:fa-github: [Github](https://github.com/marcusolsson/grafana-static-datasource)
