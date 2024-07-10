from django.db import models


class BaseManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)
