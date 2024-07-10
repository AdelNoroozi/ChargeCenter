import uuid

from django.db import models
from chargecenter.common.models import TimeStampedBaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from chargecenter.users.managers import BaseUserManager


class BaseUser(TimeStampedBaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(verbose_name=_("email"),
                              unique=True)
    is_admin = models.BooleanField(default=False, verbose_name=_("is_admin"))

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=["email"])
        ]


class SalesPerson(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(BaseUser, on_delete=models.RESTRICT, verbose_name=_("user"))
    first_name = models.CharField(max_length=256, verbose_name=_("first name"))
    last_name = models.CharField(max_length=256, verbose_name=_("last name"))
    balance = models.PositiveBigIntegerField(default=0, verbose_name=_("balance"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Sales Person")
        verbose_name_plural = _("Sales People")
        indexes = [
            models.Index(fields=["balance"]),
            models.Index(fields=["created_at"])
        ]
