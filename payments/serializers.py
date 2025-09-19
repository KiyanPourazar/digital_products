# payments/serializers.py
from rest_framework import serializers
from .models import Gateway, Payment


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ['id', 'title', 'description', 'avatar']


class PaymentSerializer(serializers.ModelSerializer):
    gateway = GatewaySerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'package',
            'gateway',
            'price',
            'status',
            'device_uuid',
            'phone_number',
            'consumed_code',
            'created_time',
            'updated_time',
        ]
        read_only_fields = ['id', 'created_time', 'updated_time']
