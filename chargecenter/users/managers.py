from django.contrib.auth.models import BaseUserManager as BUM
from django.utils.translation import gettext_lazy as _


class BaseUserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError(_("Users must have an email address"))

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            raise ValueError(_("Users must have a password"))

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user
