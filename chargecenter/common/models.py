from django.db import models
from django.utils.translation import gettext_lazy as _

from chargecenter.common.managers import BaseManager


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    position = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("position"))

    objects = BaseManager()

    def save(self, *args, **kwargs):
        if self.position == 0:
            main_fk_field = getattr(self, "main_fk_field", None)

            if main_fk_field is None:
                siblings = self.__class__.objects.all()
            else:
                siblings = self.__class__.objects.filter(**{main_fk_field: getattr(self, main_fk_field)})

            max_sibling_position = siblings.aggregate(models.Max("position"))["position__max"]
            self.position = max_sibling_position + 1 if max_sibling_position is not None else 1

        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class TimeStampedBaseModel(BaseModel):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True


class ImageIncludedBaseModel(TimeStampedBaseModel):
    image_url = models.CharField(max_length=512, verbose_name=_("image url"))
    image_alt_text = models.CharField(max_length=50, verbose_name=_("image alt text"))

    class Meta:
        abstract = True
