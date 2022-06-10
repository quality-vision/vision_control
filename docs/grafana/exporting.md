# Exporting

A large part of Vision Control is the dashboards and panels delivered with it.

Unfortunately, at this time there are problems with moving dashboards/panels from one Grafana isntance to another without copying **everything** in the Grafana database. The problem is that panel references are broken and cannot be modified from the Grafana interface. See for example [this thread on the Grafana forums](https://community.grafana.com/t/issue-with-library-panels/60101).

We have tried to mitigate this issue in two ways; firstly by creating [a gallery](gallery.md) of dashboards and panels, including their implementations. Secondly, by providing a way to run a demo instance of Grafana, with all our data available.

## Running the demo

Extract `grafana.tar.gz` (provided seperately):

```shell
$ tar -xvf grafana.tar.gz ~/Downloads/grafana
```

Generate `docker-compose.demo.yml`:

```shell
$ python3 tools/scripts/demo.py generate ~/Downloads/grafana/
```

Run the demo:

```shell
$ docker-compose -f docker-compose.demo.yml up -d
```

Populate Loki (optional):

```shell
$ LOKI_URL=http://localhost:3100 python3 tools/scripts/loki.py
```

## Plugins

There is a script, `plugins.py`, in the project root directory of the project, which can be used to install plugins on a given Grafana instance. `plugins.json` contains all plugins that we have used for Vision Control.

## Grafana Dashboard Manager

A recommended tool that can be used to export data from one Grafana instance to another is [gdg](https://github.com/esnet/gdg). It will be useful when the current issues with exporting has been solved, [and it seems to be worked on right now](https://github.com/esnet/gdg/issues/67).
