from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import validate_package_price


class Package(models.Model):
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='packages/', null=True, blank=True)  # 👈 اضافه شد
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        validators=[validate_package_price]
    )
    duration = models.PositiveIntegerField(help_text="Duration in days")
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

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
