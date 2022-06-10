import sys

import click
import sentry_sdk
from freezegun import freeze_time


@click.command()
@click.option("--sentry", default="http://localhost:7999")
@click.option("--error_type", default="Exception")
@click.option("--date", default="2022-04-19 11:00:01")
def main(sentry, error_type, date):
    """
    Function used for creating fake logs in sentry,
    error_type specifies the error being passed
    """
    excep = eval(error_type)
    freezer = freeze_time(date)
    freezer.start()
    sentry_sdk.init(sentry, traces_sample_rate=1.0)

    try:
        raise excep
    except excep as e:
        sentry_sdk.capture_exception(e)
    freezer.stop()


if __name__ == "__main__":
    main()
