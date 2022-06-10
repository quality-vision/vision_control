# Shared objects in Django

There are situations were you want to share an object between classes in Django. The object shall be instantiated, preferably not more than once and thereafter be available for others to use.

## Storing objects in AppConfig

We started by considering a solution where objects are stored as properties inside the Django app's `AppConfig` subclass. In theory, this is a good solution – there is an `Appconfig.ready` callback that will be run on application startup, the `AppConfig` is managed by Django and we don't have any globals.

Inside `apps.py`:

```python
class TestConfig(AppConfig):
    name = "test"

    def __init__(self, app_name, app_module):
        super(TestConfig, self).__init__(app_name, app_module)
        self.shared = None

    def ready(self):

        # Only run `ready` on startup and not on hot code-reloads.
        if "runserver" not in sys.argv or not os.environ.get("RUN_MAIN", None):
            return True

        # Shared objects are instantiated here.
        self.shared = SharedObject()

        return True
```

Using the shared object:

```python
# Import the instantiated AppConfigs from Django.
from django.apps import apps

# Access the shared object.
shared = apps.get_app_config("test").shared

# The shared object is now ready to be used! :)
```

A **huge** downside of this solution is that Django ignores all exceptions thrown inside `AppConfig.ready` (it seems to be related to  [either this](https://github.com/django/django/blob/439cd73c1670a2af25837149a68526fe5555399d/django/apps/registry.py#L122) or [this](https://github.com/django/django/blob/439cd73c1670a2af25837149a68526fe5555399d/django/apps/config.py#L113)). Therefore, it is not possible to indicate to the user when object instantiation goes wrong. In Vision Control, it is even neccessary, because we for example instantiate GitLab, which uses user-supplied keys.

## Dependency Injection

Using a library such as [django_injector](https://github.com/blubber/django_injector) could be further investigated. However, this particular library does not allow for passing explicit arguments to the object when it is being instantiating it, making it a non-viable alternative.

## Settings

Another solution is to directly instantiate and store objects inside the app's `settings.py`. This works, but is inconventional and [requires all shared object names to be uppercase](https://docs.djangoproject.com/en/4.0/topics/settings/#creating-your-own-settings).

## Replicating how Django does it

Django instantiates shared objects inside `__init__.py` and then they are imported as part of the module. We chose to replicate this with `services.py`. It instantiates shared objects once and exposes a controlled interface that can be imported by others.
