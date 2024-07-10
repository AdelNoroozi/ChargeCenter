from django.contrib.auth.models import BaseUserManager as BUM
from django.utils.translation import gettext_lazy as _


class BaseUserManager(BUM):
    def create_user(self, username, email, is_active=True, is_admin=False, password=None):
        if not username:
            raise ValueError(_("Users must have a username"))

        user = self.model(email=self.normalize_email(email.lower()) if email else None, is_active=is_active,
                          is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            raise ValueError(_("Users must have a password"))

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_admin(self, username, email=None, password=None):
        user = self.create_user(
            username=username,
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_user(
            username=username,
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user
