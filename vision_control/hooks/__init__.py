from django.conf import settings

import logging

log = logging.getLogger(__name__)

EVENTS = ["pipeline_events"]


def configure(gitlab):
    url = f"{settings.MIDDLEWARE_URL}/hooks/gitlab/"
    log.info(f"Configuring hooks to {url}.")

    for project_id in settings.GITLAB_PROJECT_IDS:
        project = gitlab.projects.get(project_id)
        hooks = project.hooks.list()

        log.debug(f"Configuring hooks for '{project.name}' (#{project_id}).")

        for hook in hooks:
            if hook.url == url:
                hook.token = settings.GITLAB_SECRET_TOKEN
                hook.save()
                break
        else:
            events = {f"{event}": 1 for event in EVENTS}
            project.hooks.create(
                {"url": url, "token": settings.GITLAB_SECRET_TOKEN} | events
            )
