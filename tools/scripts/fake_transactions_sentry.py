import time
import string
import logging
import datetime
import traceback
from random import choice, randint, uniform

from freezegun import freeze_time
from sentry_sdk import init, set_user, start_transaction
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

sentry_sent_logger = logging.getLogger("sentry-sent")


def before_send(event, hint):
    tb = "\n".join(traceback.format_tb(hint["exc_info"][2]))
    log_str = f"\ntraceback: {tb}\n-----"

    sentry_sent_logger.info(log_str)
    return event


def main():
    transaction_names = [
        "Spara schema",
        "Betala ut lön",
        "Logga in",
        "Lägg till ny anställd",
    ]
    sentry = (
        "https://xxxxxxx@xxxxxxx.ingest.sentry.io/xxxxxx"
    )
    status_codes = [200, 404, 401, 503]
    rand_range = randint(200, 400)

    for _ in range(rand_range):
        random_date = datetime.datetime.now() - datetime.timedelta(
            seconds=randint(0, 1209600)
        )
        freezer = freeze_time(random_date, tick=True)
        freezer.start()

        rand_user_id = randint(1, 9999)
        rand_ip = "185.196.94." + str(randint(0, 99))
        rand_name = "".join(choice(string.ascii_letters) for x in range(5))
        rand_span_waits = [round(uniform(0, 2), 2) for x in range(4)]
        rand_transaction_name = choice(transaction_names)
        rand_status = choice(status_codes)

        user = {
            "id": rand_user_id,
            "email": rand_name + "@company.com",
            "name": rand_name,
            "ip": rand_ip,
        }
        init(sentry, traces_sample_rate=1.0, debug=True, integrations=[sentry_logging])
        set_user(user)

        test_transaction = start_transaction(name=rand_transaction_name, op="http")
        span_one = test_transaction.start_child(op="http")
        span_one.set_http_status(rand_status)
        time.sleep(rand_span_waits[0])
        span_two = test_transaction.start_child(op="http")
        time.sleep(rand_span_waits[1])

        span_one.finish()
        time.sleep(rand_span_waits[2])
        span_two.set_http_status(200)
        span_two.finish()
        time.sleep(rand_span_waits[3])

        transaction_status = rand_status
        test_transaction.set_http_status(transaction_status)
        test_transaction.finish()
        freezer.stop()


if __name__ == "__main__":
    main()
