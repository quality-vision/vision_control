# Deployment

At the moment, Vision Control is hosted on a low-tier DigitalOcean droplet.

!!! warning
    There are environment variables that **must** be set for the system to work, which can be found [here](setup.md#environment-variables).

!!! tips
    An example of how Vision Control can be deployed with GitLab CI can be found in `.gitlab-ci.yml`.

## Docker Compose

Because the application is dockerized, it can be started by running `docker-compose up -d`.

| Specification             | Description |
|---------------------------|------------------------------------------------------------------|
| `docker-compose.yml`      | Run services part of Vision Control, but **not the middleware**. |
| `docker-compose.dev.yml`  | Run the middleware.                                              |
| `docker-compose.prod.yml` | Run the middleware with a WSGI server and Nginx.                 |

!!! tips
    There is a metric in `VisionControlMetricsAdapter`, `vision_control-version`, which returns the current Git revision. It can, for example, be used to make sure that a deployment was successful.

    For this to work, you need to set the `GIT_REVISION` environment variable before running the system.

        export GIT_REVISION=$(git describe --always --tags)

    If not set, `vision_control-version` will return `unknown`.

## Configuration

The Grafana/Loki/Prometheus configuration used while developing Vision Control is located in `tools/config`. It is recommended to take a look at `tools/config/grafana/provisioning/datasources/datasource.yml` for how datasources can be configured to be available when Grafana is started.
