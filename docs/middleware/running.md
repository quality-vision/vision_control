# Running

## Development

For development, you start Vision Control by running:

```shell
$ python3 manage.py runserver
```

!!! tips
    If you want to host dependencies for development purposes, `docker-compose.yml` is configured to make this easier with Docker.
    It is started by running `docker-compose up`.

## Tests

Tests are configured to be run with [pytest](https://docs.pytest.org):

```shell
$ pytest

================================================= test session starts ==================================================
platform darwin -- Python 3.10.2, pytest-7.1.2, pluggy-1.0.0
django: settings: vision_control.settings.test (from ini)
rootdir: /Users/hugolundin/Developer/school/kandidatprojekt, configfile: pyproject.toml
plugins: django-4.5.2
collected 17 items

api/grafana_json_datasource/test_datasource.py .............                                                     [ 76%]
api/tests/test_utils.py ....                                                                                     [100%]

================================================== 17 passed in 0.22s ==================================================
```

## Production

In production, Django shall be used with a [WSGI server](https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/). `docker-compose.prod.yml` has been made for this purpose.
