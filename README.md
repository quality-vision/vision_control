# Vision Control

## Setup

Install [Poetry](https://python-poetry.org) for your platform.

Instantiate a shell with the required Python version and all dependencies installed:

```shell
$ poetry install
$ poetry shell
```

Install pre-commit hooks to validate commits before they are pushed:

```shell
$ pre-commit install
```

## Usage

You can manually format the project, to pass the pre-commit hooks, by running:

```shell
$ poe format
```

Run tests with:

```shell
$ pytest
```
