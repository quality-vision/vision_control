#!/usr/bin/env python3.10
import logging

log = logging.getLogger(__name__)

import os
import sys

import click
import gitlab as gitlab_api


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
@click.argument("project_id")
@click.argument("pipeline_id")
@click.argument("user_to_assign")
@click.option("--url", default=lambda: os.environ.get("GITLAB_URL"))
@click.option("--private_token", default=lambda: os.environ.get("GITLAB_ACCESS_TOKEN"))
def main(project_id, pipeline_id, user_to_assign, url, private_token):
    gitlab = gitlab_api.Gitlab(url=url, private_token=private_token)
    gitlab.auth()

    project = gitlab.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    report_url = f"{pipeline.web_url}/test_report"

    if pipeline.ref != "main":
        sys.exit(0)

    if pipeline.status != "failed":
        sys.exit(0)

    try:
        user_id_to_assign = gitlab.users.list(username=user_to_assign)[0].get_id()
    except IndexError:
        print(f"{user_to_assign} does not exist.")
        sys.exit(1)

    issue = project.issues.create(
        {
            "title": f"Test regression on main (#{pipeline_id})",
            "description": f"[The tests failed while running pipeline #{pipeline_id} on the main branch.]({report_url})",
            "labels": ["regression", "backlog"],
            "assignee_ids": [user_id_to_assign],
        }
    )

    issue.save()


if __name__ == "__main__":
    load_env_file(path="../../.env")
    main()
