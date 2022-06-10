#!/usr/bin/env python3.10

import logging

log = logging.getLogger(__name__)

import os
import sys
import json

import click
import requests

KEYS_TO_KEEP = ["name", "id"]


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
@click.option(
    "--url",
    prompt=True,
    hide_input=False,
    confirmation_prompt=False,
    default=lambda: os.environ.get("GRAFANA_URL", ""),
)
@click.option(
    "--token",
    prompt=True,
    hide_input=False,
    confirmation_prompt=False,
    default=lambda: os.environ.get("GRAFANA_TOKEN", ""),
)
def export(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{url}/api/plugins?embedded=0", headers=headers)
    plugins = json.loads(response.text)

    for plugin in plugins:
        for key in plugin.copy().keys():
            if key not in KEYS_TO_KEEP:
                plugin.pop(key, None)

    with open("plugins.json", "w") as destination:
        json.dump(plugins, destination, indent=4)


@cli.command()
@click.option(
    "--url",
    prompt=True,
    hide_input=False,
    confirmation_prompt=False,
    default=lambda: os.environ.get("GRAFANA_URL", ""),
)
@click.option(
    "--username",
    prompt=True,
    hide_input=False,
    confirmation_prompt=False,
    default=lambda: os.environ.get("GRAFANA_USER", ""),
)
@click.option(
    "--password",
    prompt=True,
    hide_input=False,
    confirmation_prompt=False,
    default=lambda: os.environ.get("GRAFANA_PPASSWORD", ""),
)
@click.argument(
    "source",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="plugins.json",
)
def install(url, username, password, source):
    headers = {
        "Content-Type": "application/json",
    }

    auth = (username, password)

    response = requests.post(
        "http://localhost:3000/api/plugins/aceiot-svg-panel/install",
        headers=headers,
        auth=auth,
    )

    with open(source, "r") as source_file:
        plugins = json.load(source_file)

    for plugin in plugins:
        response = requests.post(
            f"{url}/api/plugins/{plugin['id']}/install", headers=headers, auth=auth
        )

        match response.status_code:
            case 0:
                pass


if __name__ == "__main__":
    cli()
