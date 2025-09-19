import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError(_('Price must be greater than zero.'))


def validate_phone_number(value):
    """
    اعتبارسنجی شماره موبایل (ایران) - بین 11 تا 13 رقم
    """
    if not str(value).isdigit():
        raise ValidationError(_('Phone number must contain only digits.'))

    length = len(str(value))
    if length < 11 or length > 13:
        raise ValidationError(_('Phone number must be between 11 and 13 digits.'))

    return value


def validate_uuid(value):
    """
    چک می‌کنه UUID معتبر باشه
    """
    uuid_regex = re.compile(
        r'^[a-fA-F0-9]{8}\-'
        r'[a-fA-F0-9]{4}\-'
        r'[a-fA-F0-9]{4}\-'
        r'[a-fA-F0-9]{4}\-'
        r'[a-fA-F0-9]{12}$'
    )
    if not uuid_regex.match(str(value)):
        raise ValidationError(_('Invalid UUID format.'))

    return value


def validate_package_price(value):
    """
    قیمت نباید منفی یا صفر باشه
    """
    if value <= 0:
        raise ValidationError(_('Price must be greater than zero.'))

    return value

def validate_amount(value):
    if value <= 0:
        raise ValidationError(_('Amount must be greater than zero.'))