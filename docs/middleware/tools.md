# Tools

To develop Vision Control the tools presented below are used 🎉

## Poetry

We use [Poetry](https://python-poetry.org) for dependency management in Python. It was chosen because it locates all project configuration in `pyproject.toml`, which is almost a standard nowadays, from our experience. Generating lock files in Poetry is significantly faster than in for example Pipenv.

## pre-commit

[pre-commit](https://pre-commit.com/) allows for adding and configuring pre-commit hooks (in Git) more easily. The following hooks are being used:

* [`isort`](#isort)
* [`black`](#black)
* `trailing-whitespace`
* `end-of-file-fixer`
* `check-added-large-files`
* `check-merge-conflict`
* `detect-private-key`
* `mixed-line-ending`

## Black

[Black](https://github.com/psf/black) is used for formatting the code and keeping it consistent with [PEP 8](https://peps.python.org/pep-0008).

## isort

[isort](https://github.com/PyCQA/isort) (*I sort your imports, so you don't have to*) is used to sort imports. For consistency, we have chosen to place Django imports at the top. By tweaking `sections` in `pyproject.toml:[tool.isort]` all imports in the whole project can be resorted by running `pre-commit run --all-files`.

## MkDocs

[MkDocs](https://www.mkdocs.org/) is used to generate a [readthedocs](https://readthedocs.org/)-themed page from the Markdown files in `docs/`.

## GitLab CI

During the project, we have used GitLab CI for continuous integration and deployment. The used configuration can be found in `.gitlab-ci.yml`. It includes the following steps:

**Step 1:** Hooks

Run pre-commit hooks (the same that is run locally before a commit). This acts as a barrier for misconfigured development environments and prevents pushed commits from not following the defined conventions.

**Step 2:** Tests

Run tests. Generate a `.xml`-test report for visualizing stats in the GitLab interface.

<span style="color: #4E8DE1">**[main]**</span> **Step 3:** Deploy

Deploy the application to a server of the project's choice, using Docker 🐳

 <span style="color: #4E8DE1">**[main]**</span> **Step 3.1:** Pages

Build and deploy this documentation to GitLab pages.


<span style="color: #4E8DE1">**[main]**</span> **Step 4:** Regression test reporting

If the [tests](#2-test) fail, an issue is created on GitLab, assigned to the project test leader. It is generated with `tools/scripts/test_fail_report.py`.
