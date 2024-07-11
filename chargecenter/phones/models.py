import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class PhoneNumber(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("name"))
    number = PhoneNumberField(verbose_name=_("number"), unique=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

