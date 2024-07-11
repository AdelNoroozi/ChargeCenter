import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from chargecenter.common.models import TimeStampedBaseModel
from chargecenter.users.models import SalesPerson


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
