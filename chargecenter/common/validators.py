import re
import uuid

import regex as re1
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
            _("password must include number"),
            code="password_must_include_number"
        )


def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            _("password must include letter"),
            code="password_must_include_letter"
        )


def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            _("password must include special char"),
            code="password_must_include_special_char"
        )


def name_validator(name):
    regex = re1.compile(r'^[\p{L}\s]+$', re.UNICODE)
    if not regex.match(name):
        raise ValidationError(
            _("Name must contain only letters and spaces, with no special characters or numbers."),
            code="invalid_name"
        )


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
