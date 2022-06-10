#!/usr/bin/env python3.10


import logging

log = logging.getLogger(__name__)


import os
import sys
import json
import random
import datetime

import click
import environ
import logging_loki
from freezegun import freeze_time

COMPANIES = [
    "Sobuli",
    "Lenas ost och kyckling",
    "Skånska grill & bar",
    "Lena R.",
    "Kalle's Musteri",
]

FEATURES = {
    "Create work shift ": {
        "steps": 4,
        "definitions": ["Open schedule", "Reserve time slot", "Save draft", "Publish"],
    },
    "Add staff": {
        "steps": 3,
        "definitions": ["Open staff", "Add staff", "Save staff member"],
    },
    "Pay wage": {
        "steps": 5,
        "definitions": [
            "Open wages",
            "Filter by unpaid",
            "Search for person",
            "Open approve",
            "Approve payment",
        ],
    },
    "Register absence": {
        "steps": 4,
        "definitions": [
            "Open times",
            "Register absence",
            "Choose reason",
            "Save absence",
        ],
    },
}


def load_env_file(path=".env"):
    try:
        for line in open(path):
            var = line.strip().split("=")
            if len(var) == 2:
                os.environ[var[0]] = var[1]
    except FileNotFoundError:
        pass
    finally:
        log.debug(f"Importing environment from {path}...")


@click.command()
@click.option("--loki", default=lambda: os.environ.get("LOKI_URL"))
@click.option("--loki_access", default=lambda: os.environ.get("LOKI_ACCESS_TOKEN"))
@click.option("--count", default=10)
def create_logs(loki, loki_access, count):
    """
    Pushes Loki logs to our test instance with manipulated timestamps.
    The timestamps are randomized and distributed over two weeks backwards
    from the current time.

    """
    log.addHandler(
        logging_loki.LokiHandler(
            url=f"{loki}/loki/api/v1/push",
            tags={"application": "company"},
            auth=("grupp13", loki_access),
            version="1",
        )
    )
    current_time = datetime.datetime.today()
    for i in range(count):
        time_step_backwards = datetime.timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 60),
        )
        new_timestamp = current_time - time_step_backwards

        with freeze_time(new_timestamp):
            print(datetime.datetime.today())
            feature = random.choice(list(FEATURES))
            requested_steps = random.randint(1, FEATURES[feature]["steps"])
            company = random.choice(COMPANIES)
            step = 1
            while requested_steps >= step:
                final_step = False
                if step == FEATURES[feature]["steps"]:
                    final_step = True
                definition = FEATURES[feature]["definitions"][step - 1]
                log.error(
                    "Test",
                    extra={
                        "tags": {
                            "company": company,
                            "feature": feature,
                            "step": step,
                            "step_definition": definition,
                            "final_step": final_step,
                            "new_tag": new_timestamp.isoformat(),
                        }
                    },
                )
                step += 1


if __name__ == "__main__":
    load_env_file(path="../../.env")
    create_logs()
