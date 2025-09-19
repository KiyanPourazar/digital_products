# payments/models.py
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from users.models import User
from subscriptions.models import Package
from utils.validators import validate_amount, validate_phone_number


class Gateway(models.Model):
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    avatar = models.ImageField(_('avatar'), upload_to='gateways/', blank=True, null=True)
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    def __str__(self):
        return self.title


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 1
    STATUS_ERROR = 2
    STATUS_CANCELED = 3
    STATUS_REFUNDED = 4

    PAYMENT_STATUS_CHOICES = (
        (STATUS_VOID, 'void'),
        (STATUS_PAID, 'paid'),
        (STATUS_ERROR, 'error'),
        (STATUS_CANCELED, 'canceled'),
        (STATUS_REFUNDED, 'refunded'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='payments')
    gateway = models.ForeignKey(Gateway, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    price = models.PositiveIntegerField(
        _('price'),
        validators=[MinValueValidator(1), validate_amount]
    )

    status = models.PositiveSmallIntegerField(
        _('status'),
        choices=PAYMENT_STATUS_CHOICES,
        default=STATUS_VOID
    )

    device_uuid = models.UUIDField(_('device uuid'), default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.BigIntegerField(_('phone number'), validators=[validate_phone_number])
    consumed_code = models.CharField(_('consumed code'), max_length=10, blank=True, null=True)
    token = models.CharField(_('token'), max_length=100, blank=True, null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.package} - {self.get_status_display()} - {self.price}"
