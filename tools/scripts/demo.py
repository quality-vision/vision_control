#!/usr/bin/env python3.10

import logging

log = logging.getLogger(__name__)

import os
import sys
import json
import inspect

import click


@click.group()
@click.option(
    "--level", type=click.Choice(logging._nameToLevel.keys()), default="WARNING"
)
def cli(level) -> None:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s: %(message)s",
        level=logging._nameToLevel[level],
    )


@cli.command()
@click.argument("source", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def generate(source):
    with open("docker-compose.demo.yml", "w") as target:
        COMPOSE = inspect.cleandoc(
            f"""
        version: '3.9'

        services:
            middleware:
                build:
                    context: .
                    dockerfile: ./vision_control/Dockerfile
                ports:
                    - "8000:8000"
                env_file:
                    - .env
                environment:
                    - GIT_REVISION
                volumes:
                    - ./vision_control:/backend
                depends_on:
                    - loki
                command: >
                    sh -c "python manage.py migrate &&
                        DJANGO_SETTINGS_MODULE=vision_control.settings.production gunicorn vision_control.wsgi:application --bind 0.0.0.0:8000"

            loki:
                image: grafana/loki:latest
                ports:
                    - "3100:3100"
                volumes:
                    - ./tools/config/loki/:/etc/loki/
                command: -config.file=/etc/loki/config.yaml

            grafana:
                image: grafana/grafana:latest
                ports:
                    - '3000:3000'
                links:
                    - loki
                    - middleware
                volumes:
                    - {source}/:/var/lib/grafana
                    - ./tools/config/grafana/provisioning/:/etc/grafana/provisioning/
                    - ./tools/config/grafana/dashboards/:/var/lib/grafana/dashboards/

            prometheus:
                image: prom/prometheus:latest
                volumes:
                    - ./tools/config/prometheus/:/etc/prometheus/
                command:
                    - '--config.file=/etc/prometheus/prometheus.yml'
                    - '--storage.tsdb.path=/prometheus'
                    - '--web.console.libraries=/etc/prometheus/console_libraries'
                    - '--web.console.templates=/etc/prometheus/consoles'
                    - '--storage.tsdb.retention=200h'
                    - '--web.enable-lifecycle'
                restart: unless-stopped
                ports:
                    - "9090:9090"
        """
        )

        target.write(COMPOSE)


if __name__ == "__main__":
    cli()
