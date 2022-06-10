# Removing mocked data

During development, mocked data was used. The following chapter describes how to modify the system to use real data instead.

!!! tips
    To make it easier, all places in the code that must be modified, have been annotated with `FIXME`.

## GitLab

There is a `FIXME` in `vision_control/api/adapters/gitlab.py:users(_)`. It suggests what to change in the code (retreive all users instead of a hard-coded list).
