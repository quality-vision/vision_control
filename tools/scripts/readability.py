#!/usr/bin/env python3.10


import os

import click
import textstat
from pyment import PyComment


class GradeLimitException(Exception):
    pass


def files(path, extension=None):
    for base, _, files in os.walk(path):
        for file_name in files:
            if extension:
                if not file_name.endswith(extension):
                    continue

            yield f"{base}/{file_name}"


def docstrings(path):
    for file in files(path, extension=".py"):
        comments = PyComment(file)

        for comment in comments.get_output_docs():
            if text := comment.replace('"""', "").strip():
                yield file, text


@click.command()
@click.option("--limit", default=0)
@click.argument("path", type=click.Path())
def main(path, limit):
    for file, docstring in docstrings(path):
        grade = textstat.flesch_kincaid_grade(docstring)

        if grade < limit:
            raise GradeLimitException(
                f"The following docstring (in {file}) has flesch kincaid grade ({grade}) below {limit}:\n\n    {docstring}\n"
            )


if __name__ == "__main__":
    main()
