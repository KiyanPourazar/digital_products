from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import validate_package_price


class Package(models.Model):
    title = models.CharField(_('package title'), max_length=100)
    sku = models.CharField(_('SKU'), max_length=50, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        validators=[validate_package_price]
    )
    duration = models.PositiveIntegerField(_('duration (days)'))
    is_enable = models.BooleanField(_('is enable'), default=True)

    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price} T"


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='subscriptions')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='subscriptions')

    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'))

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Subscription({self.user.phone_number} -> {self.package.title})"
