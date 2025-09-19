# payments/admin.py
from django.contrib import admin
from .models import Gateway, Payment

@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable', 'created_time', 'updated_time']
    search_fields = ['title']
    list_filter = ['is_enable']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'gateway', 'price', 'status', 'device_uuid', 'phone_number', 'consumed_code', 'created_time', 'updated_time']
    list_filter = ['status', 'gateway', 'package']
    search_fields = ['user__username', 'phone_number', 'device_uuid']
    readonly_fields = ['device_uuid', 'created_time', 'updated_time']
