# Architecture

Vision Control is inspired by the [layered OSI model](https://en.wikipedia.org/wiki/OSI_model) in that it is divided
into layers that each deal with different levels of abstraction. The purpose of this is to decouple each layer from each other,
allowing for changes without affecting other parts of the code base.

![Architecture](img/architecture.png)

## Layers

![Layers](img/layers.png)

### <span style="color: #575757">Layer 1</span> – HTTP Request

This layer deals directly with HTTP communication and is entirely managed by Django. No logic or data specific to Vision Control is handled here. The requests received by Django is handed to the appropriate `views.py` implementation.

**Sources:** -

### <span style="color: #E9AC10">Layer 2</span> – Body

In `views.py`, we only have knowledge about that we have received a HTTP request and that we are supposed to construct an answer. We don't know anything about what the data looks like and it isn't our responsiblity. The HTTP request body is extracted, and its JSON is deserialized. The task of constructing the response data is delegated to `GrafanaJSONDatasource.`

**Sources:** `vision_control/api/views.py`

### <span style="color: #CB6087">Layer 3</span> – Grafana Query

Layer 3 deals with parsing Grafana queries, in order to find out which metric or variable that is being requested. This layer is Grafana specific and reponsible for having knowledge about how the [JSON API Grafana Datasource plugin](../grafana/resources.md#json-api-grafana-datasource) formats its requests.

When the [`scope`](payload.md#payload) and [`target`](payload.md#payload) have been identified, the execution is dispatched to an adapter that handles fetching the data. The data will be returned either as a `Table` or as a `Timeseries`. Because the adapters have no knowledge (nor should they) about how such data should be formatted when being returned to Grafana, it is our responsability to do so here.

**Sources:** `vision_control/api/grafana_json_datasource/*`

### <span style="color: #6147AB">Layer 4</span> – Payload

The final layer knows how to parse the [payload](payload.md) in a Grafana query, which is specific for each metric provided by Vision Control. This is done via [adapters](adapters.md) which acts as the bridge between a 3rd party data source and the rest of the system.

**Sources:** `vision_control/api/adapters/*`

!!! note
    An adapter can be made to work with any data source, no matter whether it is a 3rd-party API or a local class generating some kind of data. If you wish to integrate custom data into Vision Control, the proper way to go about, is to create a new adapter class and register it in `vision_control/api/services.py` as a new metrics- or variables-adapter.

## Structure

The purpose of these graphs is to give an overview of the system and some of the dependencies between sub-systems. It has been simplified and does not contain every detail – for that, you will have to take a look at the actual code 👀

### API

<div style="text-align: center;">

```dot
digraph {
    rankdir="TB";
    graph[fontname="Courier New",size="7.7!"];
    node[fontname="Courier New", shape=box];
    edge[fontname="Courier New"];

    api [shape=component, label="API"];

    adapters [shape=folder, label="Adapters", tooltip="vision_control/api/adapters/"];
    services [shape=note, label="Services", tooltip="vision_control/api/services.py"];
    grafana_json_datasource [shape=folder, label="Grafana JSON\nDatasource", tooltip="vision_control/api/grafana_json_datasource/"];

    vision_control_adapters[shape=note, label="Vision Control\nAdapters", tooltip="vision_control/api/adapters/vision_control.py"];
    vision_control_metrics_adapter[label="Vision Control\nMetrics Adapter", tooltip="vision_control/api/adapters/vision_control.py"];

    gitlab_adapters[label="GitLab\nAdapters", shape=note, tooltip="vision_control/api/adapters/gitlab.py"];
    gitlab_metrics_adapter[label="GitLab\nMetrics Adapter", tooltip="vision_control/api/adapters/gitlab.py"];
    gitlab_variables_adapter[label="GitLab\nVariables Adapter", tooltip="vision_control/api/adapters/gitlab.py"];

    datasource[label="Datasource", shape=note, tooltip="vision_control/api/grafana_json_datasource/datasource.py"];
    GrafanaJSONDatasource[tooltip="vision_control/api/grafana_json_datasource/datasource.py"];
    exceptions[label="Exceptions", shape=note, tooltip="vision_control/api/grafana_json_datasource/exceptions.py"];
    types[label="Types", shape=note, tooltip="vision_control/api/grafana_json_datasource/types.py"];
    TableColumnType[tooltip="vision_control/api/grafana_json_datasource/types.py"];
    TableColumn[tooltip="vision_control/api/grafana_json_datasource/types.py"];
    Table[tooltip="vision_control/api/grafana_json_datasource/types.py"];
    Timeseries[tooltip="vision_control/api/grafana_json_datasource/types.py"];

    api -> services;
    api -> adapters;
    adapters -> gitlab_adapters;
    adapters -> vision_control_adapters;
    gitlab_adapters -> gitlab_metrics_adapter;
    gitlab_adapters -> gitlab_variables_adapter;
    vision_control_adapters -> vision_control_metrics_adapter;

    api -> grafana_json_datasource;
    grafana_json_datasource -> datasource;
    datasource -> GrafanaJSONDatasource;
    grafana_json_datasource -> exceptions;
    grafana_json_datasource -> types;
    types -> Table;
    types -> Timeseries;
    Table -> TableColumn;
    TableColumn -> TableColumnType;

}
```
</div>

!!! tips
    You can hover over a box to see what file it is located in.

#### Service instantiation

<div style="text-align: center;">

```dot
digraph {
    graph[fontname="Courier New",size="5!",margin="0.1 0"];
    node[fontname="Courier New", shape=box];
    edge[fontname="Courier New"];

    settings[shape=box3d, label="Settings", tooltip="vision_control/vision_control/settings/base.py"];
    services[shape=note, label="Services", tooltip="vision_control/vision_control/api/services.py"];
    gitlab[shape=signature, label="GitLab", tooltip="vision_control/vision_control/api/gitlab.py"];
    grafana_json_datasource [shape=folder, label="Grafana JSON\nDatasource", tooltip="vision_control/vision_control/api/grafana_json_datasource/"];
    adapters [shape=folder, label="Adapters", tooltip="vision_control/vision_control/api/adapters/"];

    collector[shape=point width=0.15];
    django_api_views[shape=note, label="Views", tooltip="vision_control/vision_control/api/views.py"];

    settings -> collector[arrowhead=none];
    gitlab -> collector[arrowhead=none];
    grafana_json_datasource -> collector[arrowhead=none];
    adapters -> collector[arrowhead=none];

    collector -> services;
    services -> django_api_views;
}
```
</div>

### Hooks

The `hooks` app is used for configuring and receiving webooks from GitLab.

<div style="text-align: center;">

```dot
digraph {
    graph[fontname="Courier New",size="5!",margin="0.1 0"];
    node[fontname="Courier New", shape=box];
    edge[fontname="Courier New"];

    hooks[shape=folder, label="Hooks",tooltip="vision_control/vision_control/hooks/"];
    gitlab[shape=cds, label="GitLab",tooltip="GITLAB_URL"];

    services[shape=note, label="Services", tooltip="vision_control/vision_control/api/services.py"];

    services -> hooks[label=<    <b>1.</b> hooks.configure()>];
    hooks -> gitlab[label=< <b>2.</b> Create new webhook<BR/>          with GITLAB_SECRET_TOKEN>];

    gitlab -> hooks[label=<  <b>3.</b> 200 OK>];
}
```
</div>

### Annotations

Graphs can be [annotated](https://grafana.com/docs/grafana/latest/dashboards/annotations) in Grafana with important events. In our case, we send all pipeline events from GitLab to Grafana as annotations. This makes it possible to for example, correlate feature usage with deployments (which triggers a pipeline event).

<br>
<div style="text-align: center;">
<img src="../img/annotation.png" width="50%">
<br><br>
<i>How annotations look in Grafana.</i>
</div>
<br>

Whenever a webhook with `object_kind = pipeline` is received from GitLab (on `GITLAB_URL`) the `/hooks/gitlab` endpoint is called which in turn will run `vision_control/hooks/views.py:gitlab`. It validates the received data and formats HTML for an annotation. Finally, a `POST` request is made to `GRAFANA_URL` to create the annotation.

<div style="text-align: center;">

```dot
digraph {
    rankdir="TB";
    graph[fontname="Courier New",size="5!",margin="0.1 0"];
    node[fontname="Courier New", shape=box];
    edge[fontname="Courier New"];

    gitlab[shape=cds, label="GitLab",tooltip="GITLAB_URL"];

    grafana[shape=cds, label="Grafana",tooltip="GRAFANA_URL"];

    views[shape=note, label="Hooks\nViews", tooltip="vision_control/vision_control/hooks/views.py"];

    gitlab -> views[label=< <b>1.</b>Pipeline event>];

    views -> grafana[label=< <b>2.</b>Format annotation <BR/>      and send POST request. >];
}
```

</div>
