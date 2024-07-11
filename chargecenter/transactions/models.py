import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from chargecenter.common.models import TimeStampedBaseModel
from chargecenter.users.models import SalesPerson, BaseUser


class Transaction(TimeStampedBaseModel):
    PENDING = "PND"
    DONE = "DN"
    WITHDRAWN = "WTH"
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (DONE, 'done'),
        (WITHDRAWN, 'withdrawn')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    salesperson = models.ForeignKey(SalesPerson, on_delete=models.RESTRICT, related_name="transactions",
                                    verbose_name=_("salesperson"))
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=PENDING, verbose_name=_("status"))
    amount = models.PositiveBigIntegerField(verbose_name=_("amount"))

    """is_charge field is for indicating the transaction type, if it's true then this is a charge transaction, otherwise
    it is a balance transaction"""
    is_charge = models.BooleanField(verbose_name=_("is charge"))

    def __str__(self):
        transaction_type = "selling charge" if self.is_charge else "increasing balance"
        return f"{transaction_type} - {self.salesperson.first_name} {self.salesperson.last_name} - {self.created_at}"

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        indexes = [
            models.Index(fields=["salesperson"]),
            models.Index(fields=["amount"])
        ]


class ChargeTransaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    transaction_obj = models.OneToOneField(Transaction, on_delete=models.RESTRICT, related_name="concrete_charge_obj",
                                           verbose_name=_("transaction_obj"))

    """the phone number value is saved as str instead of FK to avoid data loss after deletion of phone number objects"""
    phone_number = PhoneNumberField(verbose_name=_("number"))

    def __str__(self):
        return f"{self.transaction_obj.amount} for {self.phone_number} at {self.transaction_obj.created_at}"

    class Meta:
        verbose_name = _("Charge Transaction")
        verbose_name_plural = _("Charge Transactions")


class BalanceTransaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    transaction_obj = models.OneToOneField(Transaction, on_delete=models.RESTRICT, related_name="concrete_balance_obj",
                                           verbose_name=_("transaction_obj"))
    is_confirmed = models.BooleanField(default=False, verbose_name=_("is confirmed"))
    confirmed_by = models.ForeignKey(BaseUser, on_delete=models.RESTRICT, related_name="confirmed_transactions",
                                     blank=True, null=True, verbose_name=_("confirmed by"))

    def clean(self):
        if not self.confirmed_by.is_admin:
            raise ValidationError("only staff users can be referred as balance transactions' verifiers")

        super().clean()

    def __str__(self):
        return f"{self.transaction_obj.amount} for {self.transaction_obj.salesperson.first_name} " \
               f"{self.transaction_obj.salesperson.last_name} at {self.transaction_obj.created_at}"

    class Meta:
        verbose_name = _("Balance Transaction")
        verbose_name_plural = _("Balance Transactions")
