from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import inspect
import logging
from datetime import datetime

import requests

log = logging.getLogger(__name__)


PIPELINE_STATUS_ALLOWED = ["failed", "canceled", "cancelled", "success"]

PIPELINE_COLORS = {
    "success": "#28a745",
    "canceled": "#6c757d",
    "cancelled": "#6c757d",
    "failed": "#dc3545",
}


@csrf_exempt
def gitlab(request):
    headers = request.META
    data = json.loads(request.body.decode("utf-8"))

    remote_token = headers.get("HTTP_X_GITLAB_TOKEN")
    if not remote_token:
        log.warning(
            f"Received hook request without HTTP_X_GITLAB_TOKEN from {headers.get('Referer')}."
        )
        return HttpResponse("HTTP_X_GITLAB_TOKEN missing.", status=418)

    if remote_token != settings.GITLAB_SECRET_TOKEN:
        log.warning(
            f"Received hook request with invalid token from {headers.get('Referer')}."
        )
        return HttpResponse("Invalid token", status=401)

    try:
        object_kind = data["object_kind"]
        if object_kind != "pipeline":
            return HttpResponse(status=200)

        attributes = data["object_attributes"]
        pipeline_status = attributes["status"]
        pipeline_id = attributes["id"]

        pipeline_created_at = attributes["created_at"]
        if not pipeline_created_at:
            return HttpResponse(status=200)

        pipeline_finished_at = attributes["finished_at"]
        if not pipeline_finished_at:
            return HttpResponse(status=200)

        try:
            pipeline_created_at = datetime.strptime(
                pipeline_created_at, "%Y-%m-%d %H:%M:%S %Z"
            )
        except ValueError:
            return HttpResponse(status=200)

        try:
            pipeline_finished_at = datetime.strptime(
                pipeline_finished_at, "%Y-%m-%d %H:%M:%S %Z"
            )
        except ValueError:
            return HttpResponse(status=200)

        ref = attributes["ref"]
        project = data["project"]
        project_id = project["id"]
        project_web_url = project["web_url"]
        user = data["user"]

    except KeyError:
        return HttpResponse(status=200)

    user_fullname = user.get("name")
    user_name = user.get("username")
    user_avatar_url = user.get("avatar_url")
    user_profile_url = f"{settings.GITLAB_URL}/{user_name}"

    commit = data.get("commit")
    commit_id = commit.get("id")
    commit_title = commit.get("title")
    committer_author = commit.get("author")

    commit_url = commit.get("url")
    pipeline_url = f"{project_web_url}/-/pipelines/{pipeline_id}"

    if pipeline_status not in PIPELINE_STATUS_ALLOWED:
        return HttpResponse(status=200)

    html = inspect.cleandoc(
        f"""
        <div style="display: flex; margin-bottom: 8px;">
            <div>
                <img
                src="{user_avatar_url}"
                width="40px"
                />
            </div>
            <div style="text-align: left; margin-left: 10px; width: 100%;">
                <b>
                    Pipeline <a target="_blank" href="{pipeline_url}">#{pipeline_id}</a>
                </b>
                </br>
                Triggered by <a target="_blank" href="{user_profile_url}">{user_fullname}</a>
            </div>
            <div>
                <span style="background-color: {PIPELINE_COLORS[pipeline_status]}; padding: 2px 3px; border-radius: 3px; color: white;">{pipeline_status}</span>
            </div>
        </div>
        <div style="margin-bottom: 8px; border-top: 1px solid rgba(204, 204, 220, 0.07); padding-top: 5px;">
            <b>Commit</b> <a target="_blank" href="{commit_url}">{commit_id}</a> by <a href="mailto:{committer_author.get("email")}">{committer_author.get("name")}</a></br>
            {commit_title}
        </div>
    """
    )

    annotation = json.dumps(
        {
            "time": int(pipeline_created_at.timestamp()) * 1000,
            "timeEnd": int(pipeline_finished_at.timestamp()) * 1000,
            "tags": [
                f"{project_id}",
                "project",
                "pipeline",
                pipeline_status,
                ref,
                user_name,
                user_fullname,
            ],
            "text": html,
        }
    )

    headers = {
        "Authorization": f"Bearer {settings.GRAFANA_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{settings.GRAFANA_URL}/api/annotations", headers=headers, data=annotation
    )

    if response.status_code != 200:
        log.warning(
            f"Annotation request to Grafana returned {response.status_code}: {response}"
        )
        return HttpResponse(status=500)

    log.debug(f"Added annotation for #{project_id}.")

    return HttpResponse(status=200)
