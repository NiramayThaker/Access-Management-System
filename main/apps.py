from django.apps import AppConfig
from django.conf import settings


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"


# ready method is invoked when app is ready to run
    def ready(self):
        # Has to import inside so it gets load every time when function is triggered
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save

        # Will take to arguments **kwargs has user info
        def add_to_default_group(sender, **kwargs):
            # It will check for instance
            user = kwargs['instance']

            if kwargs['created']:
                # Group obj is returned or created of name="zyx" group
                group, ok = Group.objects.get_or_create(name="default")
                # Adding user to that specific group
                group.user_set.add(user)

        # Every time when there is some change in AUTH_USER_MODEL at that time function "add_to_default_group" will be called
        post_save.connect(add_to_default_group,
                  sender=settings.AUTH_USER_MODEL)
